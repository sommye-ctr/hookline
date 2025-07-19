import type {ColumnDef} from "@tanstack/react-table";

export interface WorkflowModel {
    id: number;
    name: string;
    description: string;
    isActive: boolean;
    actions: string[];
    executionCount: number;
    lastExecution: Date;
    triggers: string[];
}

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
