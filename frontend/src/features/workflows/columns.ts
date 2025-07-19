import type {ColumnDef} from "@tanstack/react-table";
import type {WorkflowModel} from "@/models/WorkflowModel.ts";

export const columns: ColumnDef<WorkflowModel>[] = [
    {
        accessorKey: "name",
        header: "Name",
    },
    {
        accessorKey: "isActive",
        header: "Status",
    },
    {
        accessorKey: "triggers",
        header: "Triggers",
    },
    {
        accessorKey: "actions",
        header: "Actions",
    },
    {
        accessorKey: "executionCount",
        header: "Executions",
    },
    {
        accessorKey: "lastExecution",
        header: "Last Run",
    }
];
