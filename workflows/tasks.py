from celery import shared_task
from django.core.exceptions import ValidationError
from hookline_sdk.registry import HooklinePlugin

from workflows.models import ExecutionLog, Workflow, Trigger, InstalledPlugin
from workflows.serializers import TriggerSerializer, ActionSerializer
from workflows.trigger_registry import TriggerMatcher
from workflows.utils import load_action_plugin

import logging
import environ

logger = logging.getLogger(__name__)
env = environ.Env()
max_retries = int(env('ACTION_MAX_RETRIES'))


def execution_log(workflow_id, status, **kwargs):
    ExecutionLog.log_entry(
        workflow_id=workflow_id,
        status=status,
        detail=kwargs
    )


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
            execution_log(workflow_id, ExecutionLog.TRIGGER_MATCHED, payload=payload, event_type=event_type,
                          triggers=TriggerSerializer(trigger).data)

            for action in wf.actions.all().order_by("order"):
                action_data = ActionSerializer(action).data

                execute_actions.delay(
                    action_data=action_data,
                    workflow_id=workflow_id,
                    payload=payload,
                    workspace_id=workspace_id,
                )
                execution_log(workflow_id, ExecutionLog.ACTION_ENQUEUED, action=action_data, triggered_by=trigger_id,
                              event_type=event_type)

        except (Trigger.DoesNotExist, Workflow.DoesNotExist) as e:
            logger.error("Something went wrong with trigger registry")
            execution_log(workflow_id, ExecutionLog.INTERNAL_ERROR, error=e)
            raise

    except Exception as e:
        logger.error("There was an error with trigger registry", e)


@shared_task(
    bind=True,
    retry_kwargs={"max_retries": max_retries}
)
def execute_actions(self, action_data, workflow_id, payload, workspace_id):
    execution_log(workflow_id, ExecutionLog.ACTION_STARTED)

    try:
        action = ActionSerializer(data=action_data)
        action.is_valid(raise_exception=True)
        action = action.validated_data

        installed_p = (InstalledPlugin.objects.filter(workspace_id=workspace_id, slug=action['type'])
                       .values_list("slug", "version").first())
        if installed_p is None:
            err = f"The plugin is not installed for action {action['type']}"
            logger.error(err)
            execution_log(workflow_id, ExecutionLog.INTERNAL_ERROR, action=action_data, message=err)
            return

        plugin: HooklinePlugin = load_action_plugin(action['type'])(installed_p[1])
        output = plugin.start(payload, action['config'])

        if (not isinstance(output, dict)
                or not all(key in output for key in ['message', 'status', 'status_code'])):
            logger.error(f"Plugin returned malformed response! with output {output}")
            execution_log(workflow_id, ExecutionLog.PLUGIN_PROTOCOL_ERROR, action=action_data, plugin_output=output,
                          message="The plugin returned malformed response")
            return

        if output.get("status") != 'success':
            execution_log(workflow_id, ExecutionLog.ACTION_FAILED, action=action_data, plugin_output=output)
            logger.error("The action failed", output.get("status"))
            return

        execution_log(workflow_id, ExecutionLog.ACTION_COMPLETED, action=action_data, plugin_output=output,
                      retry_count=self.request.retries)

    except ValidationError as e:
        logger.error(f"There was error while deserializing the action", action_data, e)
        execution_log(workflow_id, ExecutionLog.INTERNAL_ERROR, action=action_data, error=e.error_dict)
        raise
    except (FileNotFoundError, NotADirectoryError, FileNotFoundError, ImportError) as e:
        logger.error(f"There was an error in the plugin", action_data, e)
        execution_log(workflow_id, ExecutionLog.INTERNAL_ERROR, action=action_data, error=e,
                      message=f"There was an error in loading plugin {action_data['type']}")
        raise
    except AttributeError as e:
        logger.error(e)
        execution_log(workflow_id, ExecutionLog.PLUGIN_PROTOCOL_ERROR, action=action_data,
                      message="The plugin does not have create_plugin() method")
        raise
    except Exception as e:
        logger.error("Unknown error", e)
        execution_log(workflow_id, ExecutionLog.INTERNAL_ERROR, action=action_data, error=e)

        if self.request.retries < max_retries:
            logger.debug("Retrying action...", action_data)
            execution_log(workflow_id, ExecutionLog.RETRY_SCHEDULED, action=action_data, reason=e,
                          retry_count=self.request.retries)
            raise self.retry(exc=e)
        else:
            execution_log(workflow_id, ExecutionLog.RETRY_FAILED, action=action_data, reason=e,
                          retry_count=self.request.retries)
