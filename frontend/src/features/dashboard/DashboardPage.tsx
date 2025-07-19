import {LucideCircleAlert, LucideCircleCheckBig, LucideWorkflow} from "lucide-react";
import StatsCard from "@/features/dashboard/components/StatsCard.tsx";
import ListContentCard from "@/features/dashboard/components/ListContentCard.tsx";
import PageHeading from "@/components/shared/PageHeading.tsx";


const DashboardPage = () => {
    return (
        <>
            <PageHeading heading="Dashboard" buttonIcon={<LucideWorkflow/>} buttonText="New Workflow"/>

            <main>
                <div className="grid grid-cols-3 gap-7">
                    <StatsCard title="Active Workflows" description="8 workflows executed today" color='chart-1'/>
                    <StatsCard title="Total Executions" description="+18% from last week" color='chart-2'/>
                    <StatsCard title="Error Rate" description="3 errors in the last 24 hours" color='chart-5'/>
                </div>

                <div className="grid grid-cols-3 mt-8 gap-7 items-start">
                    <ListContentCard
                        className="col-span-2"
                        title="Recent Executions"
                        actionText="View all"
                        content={[
                            {
                                title: "Slack Notifications",
                                icon: <LucideCircleCheckBig color="green"/>,
                                desc: "New Message",
                                value: "12 min"
                            },
                            {
                                title: "Github PR Notifications",
                                icon: <LucideCircleAlert color="red"/>,
                                desc: "Pull Request Opened",
                                value: "19 min"
                            },
                        ]}/>

                    <ListContentCard
                        className="col-span-1"
                        title="Suggested Plugins"
                        actionText="Browse all"
                        content={[
                            {
                                title: "Slack Integration",
                                icon: "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Slack_icon_2019.svg/2048px-Slack_icon_2019.svg.png",
                                desc: "Post messages to channels when events occur"
                            },
                            {
                                title: "Github",
                                icon: "https://cdn-icons-png.flaticon.com/512/25/25231.png",
                                desc: "Automate your github workflows with hooks"
                            },
                            {
                                title: "Trello",
                                icon: "https://flow-in-public.nimbuspop.com/flow-apps/trello.png",
                                desc: "Automate creation of trello cards when events occur"
                            },
                        ]}/>
                </div>
            </main>
        </>
    )
}

export default DashboardPage;
