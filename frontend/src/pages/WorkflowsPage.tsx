import PageHeading from "@/components/PageHeading.tsx";
import {LucidePlus, LucideSearch} from "lucide-react";
import {Input} from "@/components/ui/input.tsx";
import {columns} from "@/models/WorkflowModel.ts";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";
import {DataTable} from "@/components/DataTable.tsx";

const WorkflowsPage = () => (
    <>
        <PageHeading heading="Workflows" buttonIcon={<LucidePlus/>} buttonText="New Workflow"/>

        <div className="flex justify-between gap-4">

            <div className="relative w-full">
                <Input className="pl-8" placeholder="Search workflows..."/>
                <LucideSearch className="absolute top-1/2 left-2 size-4 -translate-y-1/2 opacity-50 select-none"/>
            </div>

            <Select defaultValue="all">
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
            className="max-w-full mt-8"
            columns={columns}
            data={[
                {
                    id: 1,
                    name: "Slack Notifications",
                    description: "Send a message to a slack channel when a new event occurs",
                    isActive: true,
                    lastExecution: new Date(),
                    actions: ["Email"],
                    triggers: ["Trello"],
                    executionCount: 4,
                },
            ]}
        />
    </>
);

export default WorkflowsPage;