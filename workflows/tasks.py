from celery import shared_task

from workflows.models import ExecutionLog, Workflow, Action
from workflows.trigger_registry import TriggerMatcher
from workflows.utils import get_log_details_for_action


@shared_task
def log_event_task(workspace_id, payload, event_type):
    matcher = TriggerMatcher(payload, workspace_id, event_type)
    workflow_id = matcher.match()

    if workflow_id is None:
        print("NO match")
        return "NO MATCH"

    #logging event
    ExecutionLog.objects.create(workflow_id=workflow_id, status=ExecutionLog.TRIGGER_MATCHED)

    try:
        wf = Workflow.objects.get(pk=workflow_id)
        for action in wf.actions.all():
            print(action)
            execute_actions.delay(action.id, wf.id, payload)
            #logging event
            ExecutionLog.objects.create(
                workflow_id=workflow_id,
                status=ExecutionLog.ACTION_ENQUEUED,
                details=get_log_details_for_action(action)
            )

        return "Success!"
    except Exception as e:
        print(e)
        ExecutionLog.objects.create(workflow_id=workflow_id, status=ExecutionLog.INTERNAL_ERROR)



@shared_task
def execute_actions(action_id, workflow_id, payload):
    ExecutionLog.objects.create(
        workflow_id=workflow_id,
        status=ExecutionLog.ACTION_STARTED
    )

    print(f'{workflow_id}: {action_id} - Action executing...')
    ExecutionLog.objects.create(
        workflow_id=workflow_id,
        status=ExecutionLog.ACTION_COMPLETED
    )

