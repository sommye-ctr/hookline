import type {ColumnDef} from "@tanstack/react-table";
import type {WorkflowModel} from "@/features/workflows/types.ts";
import {Badge} from "@/components/ui/badge.tsx";
import {cn} from "@/lib/utils.ts";
import {formatDistanceToNow} from "date-fns";
import {LucideWorkflow} from "lucide-react";

export const columns: ColumnDef<WorkflowModel>[] = [
    {
        accessorKey: "name",
        header: "Name",
        accessorFn: (row) => ({
            name: row.name,
            description: row.description,
        }),
        cell: ({getValue}) => {
            const {name, description} = getValue() as { name: string, description: string }
            return (
                <div className="flex items-center gap-2">
                    <LucideWorkflow className="h-6 w-6"/>
                    <div className="flex flex-col">
                        <span className="text-sm">{name}</span>
                        <span className="text-xs text-muted-foreground">{description}</span>
                    </div>
                </div>
            )
        }
    },
    {
        accessorKey: "triggers",
        header: "Triggers",
        cell: ({row}) => {
            const triggers: string[] = row.getValue("triggers")
            return (
                <div className="flex gap-2 flex-wrap">
                    {triggers.map((trigger) => (
                        <Badge key={trigger}>
                            {trigger}
                        </Badge>
                    ))}
                </div>
            )
        }
    },
    {
        accessorKey: "actions",
        header: "Actions",
        cell: ({row}) => {
            const actions: string[] = row.getValue("actions")
            return (
                <div className="flex gap-2 flex-wrap">
                    {actions.map((action) => (
                        <Badge key={action} variant="outline">
                            {action}
                        </Badge>
                    ))}
                </div>
            )
        }
    },
    {
        accessorKey: "isActive",
        header: "Status",
        cell: ({row}) => {
            const status: boolean = row.getValue("isActive")

            return (
                <div className="flex items-center gap-2">
          <span
              className={cn(
                  "h-2 w-2 rounded-full",
                  status ? "bg-green-500" : "bg-red-500"
              )}
          />
                    <span>{status ? "Active" : "Inactive"}</span>
                </div>
            )
        }
    },
    {
        accessorKey: "lastExecution",
        header: "Last Run",
        cell: ({row}) => {
            const lastExecution: string = row.getValue("lastExecution")
            const date: Date = new Date(lastExecution)
            return <span>{formatDistanceToNow(date, {addSuffix: true})}</span>
        }
    },
    {
        accessorKey: "executionCount",
        header: "Executions",
    },
];
