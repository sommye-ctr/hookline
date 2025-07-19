import * as React from "react"
import {
    LucideBlocks,
    LucideLayoutDashboard, LucideLogs,
    LucideWorkflow, LucideZap,
} from "lucide-react"

import {NavMain} from "@/components/nav-main"
import {NavUser} from "@/components/nav-user"
import {WorkspaceSwitcher} from "@/components/workspace-switcher.tsx"
import {Sidebar, SidebarContent, SidebarFooter, SidebarHeader, SidebarRail,} from "@/components/ui/sidebar"

const data = {
    user: {
        name: "shadcn",
        email: "m@example.com",
    },
    teams: [
        {name: "Acme Inc"},
        {name: "Acme Corp."},
        {name: "Evil Corp."},
    ],
    navMain: [
        {
            title: "Dashboard",
            url: "",
            icon: LucideLayoutDashboard,
            isActive: true,
        },
        {
            title: "Workflows",
            url: "workflows",
            icon: LucideWorkflow,
        },
        {
            title: "Plugins",
            url: "#",
            icon: LucideBlocks,
        },
        {
            title: "Triggers",
            url: "#",
            icon: LucideZap,
        },
        {
            title: "Execution Logs",
            url: "#",
            icon: LucideLogs,
        },
    ],
}

export function AppSidebar({...props}: React.ComponentProps<typeof Sidebar>) {
    return (
        <Sidebar collapsible="icon" {...props}>
            <SidebarHeader>
                <WorkspaceSwitcher teams={data.teams}/>
            </SidebarHeader>
            <SidebarContent>
                <NavMain items={data.navMain}/>
            </SidebarContent>
            <SidebarFooter>
                <NavUser user={data.user}/>
            </SidebarFooter>
            <SidebarRail/>
        </Sidebar>
    )
}
