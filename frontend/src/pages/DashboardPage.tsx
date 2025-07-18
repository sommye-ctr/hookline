import {AppSidebar} from "@/components/app-sidebar"
import {SidebarInset, SidebarProvider, SidebarTrigger,} from "@/components/ui/sidebar"
import {Input} from "@/components/ui/input.tsx";
import {LucideBell, LucideSearch, LucideWorkflow} from "lucide-react";
import {Button} from "@/components/ui/button.tsx";
import SearchDialog from "@/components/SearchDialog.tsx";
import {useState} from "react";
import StatsCard from "@/components/StatsCard.tsx";


const DashboardPage = () => {
    const [searchOpen, setSearchOpen] = useState(false);

    return (
        <SidebarProvider>
            <AppSidebar/>
            <SidebarInset>
                <header
                    className="flex shrink-0 items-center justify-between gap-2 transition-[width,height] ease-linear">
                    <div className="ml-4 flex items-center gap-4">
                        <SidebarTrigger/>
                        <h3 className="text-primary">Hookline</h3>
                    </div>
                    <div className="relative mx-auto w-1/4">
                        <Input type="search" placeholder="Search..."
                               readOnly={true}
                               className="border-none pl-8 focus:border-none bg-gray-300"
                               onClick={() => setSearchOpen(true)}/>
                        <SearchDialog open={searchOpen} onOpenChange={setSearchOpen}/>
                        <LucideSearch
                            className="pointer-events-none absolute top-1/2 left-2 size-4 -translate-y-1/2 opacity-50 select-none"/>
                    </div>

                    <Button variant="ghost" size="icon" className="size-7 mr-4">
                        <LucideBell className="size-5"/>
                    </Button>
                </header>

                <div className="flex justify-between m-5">
                    <h3>Dashboard</h3>
                    <Button>
                        <LucideWorkflow/>
                        New Workflow
                    </Button>
                </div>

                <main className="mx-5">
                    <div className="grid grid-cols-3 gap-3">
                        <StatsCard title="Active Workflows" description="8 workflows executed today" color='chart-1'/>
                        <StatsCard title="Total Executions" description="+18% from last week" color='chart-2'/>
                        <StatsCard title="Error Rate" description="3 errors in the last 24 hours" color='chart-5'/>
                    </div>
                </main>
            </SidebarInset>
        </SidebarProvider>
    )
}

export default DashboardPage;
