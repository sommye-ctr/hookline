"use client"

import {type LucideIcon} from "lucide-react"
import {SidebarGroup, SidebarMenu, SidebarMenuButton, SidebarMenuItem,} from "@/components/ui/sidebar.tsx"
import {Link} from "react-router";

export function NavMain({
                            items,
                        }: {
    items: {
        title: string
        url: string
        icon?: LucideIcon
        isActive?: boolean
        items?: {
            title: string
            url: string
        }[]
    }[]
}) {
    return <SidebarGroup>
        <SidebarMenu>
            {items.map((item) => <Link to={item.url}>
                <SidebarMenuItem key={item.title} className="items-center justify-center">
                    <SidebarMenuButton tooltip={item.title} size="lg" className="m-0">
                        <div className="text-muted-foreground">
                            {item.icon && <item.icon/>}
                        </div>
                        <span className="text-lg">{item.title}</span>
                    </SidebarMenuButton>
                </SidebarMenuItem>
            </Link>)}
        </SidebarMenu>
    </SidebarGroup>
}
