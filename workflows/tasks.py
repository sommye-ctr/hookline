from celery import shared_task

from workflows.models import ExecutionLog, Workflow
from workflows.trigger_registry import TriggerMatcher
from workflows.utils import get_log_details_for_action

import logging
import environ
logger = logging.getLogger(__name__)
env = environ.Env()


@shared_task
def log_event_task(workspace_id, payload, event_type):
    matcher = TriggerMatcher(payload, workspace_id, event_type)
    workflow_id = matcher.match()

    if workflow_id is None:
        logger.debug("No match!")
        return "NO MATCH"

    #logging event
    ExecutionLog.objects.create(workflow_id=workflow_id, status=ExecutionLog.TRIGGER_MATCHED)

    try:
        wf = Workflow.objects.get(pk=workflow_id)
        for action in wf.actions.all():
            execute_actions.delay(action.id, wf.id)
            #logging event
            ExecutionLog.objects.create(
                workflow_id=workflow_id,
                status=ExecutionLog.ACTION_ENQUEUED,
                details=get_log_details_for_action(action)
            )
        return "Success!"
    except Exception as e:
        ExecutionLog.objects.create(workflow_id=workflow_id, status=ExecutionLog.INTERNAL_ERROR)
        logger.exception(e)



@shared_task(
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries":int(env('ACTION_MAX_RETRIES'))}
)
def execute_actions(action_id, workflow_id):
    ExecutionLog.objects.create(
        workflow_id=workflow_id,
        status=ExecutionLog.ACTION_STARTED
    )

    #TODO - Error handling in here...

    print(f'{workflow_id}: {action_id} - Action executing...')
    ExecutionLog.objects.create(
        workflow_id=workflow_id,
        status=ExecutionLog.ACTION_COMPLETED
    )

