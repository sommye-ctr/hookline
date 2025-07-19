import PageHeading from "@/components/PageHeading.tsx";
import {LucidePlus, LucideSearch} from "lucide-react";
import {Input} from "@/components/ui/input.tsx";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectLabel,
    SelectTrigger,
    SelectValue
} from "@/components/ui/select";

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
                    <SelectValue />
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
    </>
);

export default WorkflowsPage;