import {AppSidebar} from "@/components/app-sidebar"
import {SidebarInset, SidebarProvider, SidebarTrigger,} from "@/components/ui/sidebar"
import {Input} from "@/components/ui/input.tsx";
import {LucideBell, LucideSearch} from "lucide-react";
import {Button} from "@/components/ui/button.tsx";
import SearchDialog from "@/components/SearchDialog.tsx";
import {useState} from "react";


const DashboardPage = () => {
    const [searchOpen, setSearchOpen] = useState(false);

    return (
        <SidebarProvider>
            <AppSidebar/>
            <SidebarInset>
                <header
                    className="mx-1 flex shrink-0 items-center justify-between gap-2 transition-[width,height] ease-linear">
                    <div className="flex items-center gap-4 px-4">
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

                    <Button variant="ghost" size="icon" className="size-7">
                        <LucideBell className="size-5"/>
                    </Button>
                </header>
            </SidebarInset>
        </SidebarProvider>
    )
}

export default DashboardPage;
