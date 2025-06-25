from celery import shared_task
from django.core.exceptions import ValidationError

from workflows.models import ExecutionLog, Workflow, Trigger
from workflows.serializers import TriggerSerializer, ActionSerializer
from workflows.trigger_registry import TriggerMatcher
from workflows.utils import load_action_plugin

import logging
import environ

logger = logging.getLogger(__name__)
env = environ.Env()
max_retries = int(env('ACTION_MAX_RETRIES'))


@shared_task
def log_event_task(workspace_id, payload, event_type):
    matcher = TriggerMatcher(payload, workspace_id, event_type)

    try:
        workflow_id, trigger_id = matcher.match()

        if workflow_id is None:
            logger.debug(f"No match for event:{event_type} & workspace:{workspace_id}")
            return

        try:
            trigger = Trigger.objects.get(pk=trigger_id)
            wf = Workflow.objects.get(pk=workflow_id)

            ExecutionLog.log_entry(
                workflow_id=workflow_id,
                status=ExecutionLog.TRIGGER_MATCHED,
                detail={
                    "payload": payload,
                    "event_type": event_type,
                    "triggers": TriggerSerializer(trigger).data
                }
            )

            for action in wf.actions.all().order_by("order"):
                action_data = ActionSerializer(action).data

                execute_actions.delay(
                    action_data=action_data,
                    workflow_id=workflow_id,
                    payload=payload,
                )
                ExecutionLog.log_entry(
                    workflow_id=workflow_id,
                    status=ExecutionLog.ACTION_ENQUEUED,
                    detail={
                        "action": action_data,
                        "event_context": {
                            "triggered_by": trigger_id,
                            "event_type": event_type
                        }
                    }
                )
        except Trigger.DoesNotExist | Workflow.DoesNotExist as e:
            logger.error("Something went wrong with trigger registry")
            ExecutionLog.log_entry(
                workflow_id=workflow_id,
                status=ExecutionLog.INTERNAL_ERROR,
                detail={"error": e.__dict__}
            )
            raise

    except Exception as e:
        logger.error("There was an error with trigger registry", e)


@shared_task(
    bind=True,
    retry_kwargs={"max_retries": max_retries}
)
def execute_actions(self, action_data, workflow_id, payload):
    ExecutionLog.objects.create(
        workflow_id=workflow_id,
        status=ExecutionLog.ACTION_STARTED
    )

    try:
        action = ActionSerializer(data=action_data)
        action.is_valid(raise_exception=True)
        action = action.save(commit=False)

        execute = load_action_plugin(action.type)
        output = execute(payload, action.config)

        if not isinstance(output, dict) or not any(
                hasattr(output, attr) for attr in ['message', 'status', 'status_code']):
            logger.error("Plugin returned malformed response!")
            ExecutionLog.objects.create(
                workflow_id=workflow_id,
                status=ExecutionLog.PLUGIN_PROTOCOL_ERROR,
                detail={
                    "action": action_data,
                    "plugin_output": str(output),
                    "message": "The plugin returned malformed response"
                }
            )
            return

        if output.get("status") != 'success':
            ExecutionLog.objects.create(
                workflow_id=workflow_id,
                status=ExecutionLog.ACTION_FAILED,
                detail={
                    "action": action_data,
                    "plugin_output": output,
                }
            )
            logger.error("The action failed", output.get("status"))
            return

        ExecutionLog.objects.create(
            workflow_id=workflow_id,
            status=ExecutionLog.ACTION_COMPLETED,
            detail={
                "action": action_data,
                "plugin_output": output,
                "retry_count" : self.request.retries,
            }
        )

    except ValidationError as e:
        logger.error(f"There was error while deserializing the action", action_data, e)
        ExecutionLog.log_entry(
            workflow_id=workflow_id,
            status=ExecutionLog.INTERNAL_ERROR,
            detail={
                "action": action_data,
                "error": e.error_dict
            }
        )
        return
    except (FileNotFoundError, NotADirectoryError, FileNotFoundError, AttributeError, ImportError) as e:
        logger.error(f"There was an error in the plugin", action_data, e)
        ExecutionLog.log_entry(
            workflow_id=workflow_id,
            status=ExecutionLog.INTERNAL_ERROR,
            detail={
                "action": action_data,
                "error": e.__dict__,
                "message": f"There was an error in loading plugin {action_data['type']}"
            }
        )
        raise
    except Exception as e:
        logger.error("Unknown error", e)
        ExecutionLog.log_entry(
            workflow_id=workflow_id,
            status=ExecutionLog.INTERNAL_ERROR,
            detail={
                "action": action_data,
                "error": e.__dict__
            }
        )
        if self.request.retries < max_retries:
            logger.debug("Retrying action...", action_data)
            ExecutionLog.log_entry(
                workflow_id=workflow_id,
                status=ExecutionLog.RETRY_SCHEDULED,
                detail={
                    "action": action_data,
                    "reason": e.__dict__,
                    "retry_count": self.request.retries
                }
            )
            raise self.retry(exc=e)
        else:
            ExecutionLog.log_entry(
                workflow_id=workflow_id,
                status=ExecutionLog.RETRY_FAILED,
                detail={
                    "action": action_data,
                    "reason": e.__dict__,
                    "retry_count": self.request.retries
                }
            )
