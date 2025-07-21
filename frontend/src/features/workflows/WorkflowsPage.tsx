import PageHeading from "@/components/shared/PageHeading.tsx";
import {LucidePlus, LucideSearch} from "lucide-react";
import {DataTable} from "@/components/shared/DataTable.tsx";
import {columns} from "@/features/workflows/columns.tsx";
import {useState} from "react";
import type {ColumnFiltersState} from "@tanstack/react-table";
import {Input} from "@/components/ui/input.tsx";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select.tsx";
import {Card, CardContent} from "@/components/ui/card.tsx";

const WorkflowsPage = () => {
    const [filters, setFilters] = useState<ColumnFiltersState>([]);

    const handleFilterChange = (value: string) => {
        console.log(value);
        setFilters(prev => [
            ...prev.filter(f => f.id !== "name"),
            {id: "name", value},
        ]);
    };

    const setStatusFilter = (value: boolean) => {
        setFilters(prev => [
            ...prev.filter(f => f.id !== "isActive"),
            {id: "isActive", value: value},
        ]);
    }

    const handleStatusChange = (value: string) => {
        if (value === "all") {
            setFilters([]);
        } else if (value === "active") {
            setStatusFilter(true);
        } else {
            setStatusFilter(false);
        }
    }

    return (
        <>
            <PageHeading heading="Workflows" buttonIcon={<LucidePlus/>} buttonText="New Workflow"/>

            <Card className="p-0">
                <CardContent className="p-0">
                    <div className="flex justify-between gap-4 m-4">

                        <div className="relative w-full">
                            <Input
                                className="pl-8"
                                placeholder="Search workflows..."
                                onChange={(e) => handleFilterChange(e.target.value)}
                            />
                            <LucideSearch
                                className="absolute top-1/2 left-2 size-4 -translate-y-1/2 opacity-50 select-none"/>
                        </div>

                        <Select defaultValue="all" onValueChange={handleStatusChange}>
                            <SelectTrigger className="w-[180px]">
                                <SelectValue/>
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                    <SelectLabel>Filter</SelectLabel>
                                    <SelectItem value="all">All Workflows</SelectItem>
                                    <SelectItem value="active">Active Workflows</SelectItem>
                                    <SelectItem value="inactive">Inactive Workflows</SelectItem>
                                </SelectGroup>
                            </SelectContent>
                        </Select>

                    </div>

                    <DataTable
                        filters={filters}
                        setFilters={setFilters}
                        className="max-w-full rounded-b-md"
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
                </CardContent>
            </Card>
        </>
    );
}

export default WorkflowsPage;