import PageHeading from "@/components/shared/PageHeading.tsx";
import {LucidePlus} from "lucide-react";
import {DataTable} from "@/components/shared/DataTable.tsx";
import {columns} from "@/features/workflows/columns.tsx";

const WorkflowsPage = () => {


    return (
        <>
            <PageHeading heading="Workflows" buttonIcon={<LucidePlus/>} buttonText="New Workflow"/>

            <DataTable
                className="max-w-full mt-4"
                columns={columns}
                data={[
                    {
                        id: 1,
                        name: "Slack Notifications",
                        description: "Send a message to a slack channel when a new event occurs",
                        isActive: true,
                        lastExecution: new Date(),
                        actions: ["Email", "Slack", "Issue"],
                        triggers: ["Trello"],
                        executionCount: 4,
                    },
                    {
                        id: 2,
                        name: "Github Issues",
                        description: "Send a message to a slack channel when a new event occurs",
                        isActive: false,
                        lastExecution: new Date(),
                        actions: ["Email", "Slack", "Issue"],
                        triggers: ["Trello"],
                        executionCount: 4,
                    },
                ]}
            />
        </>
    );
}

export default WorkflowsPage;