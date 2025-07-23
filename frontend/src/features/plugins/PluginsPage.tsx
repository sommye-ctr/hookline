import PageHeading from "@/components/shared/PageHeading.tsx";
import {Card, CardContent} from "@/components/ui/card.tsx";
import IconInput from "@/components/shared/IconInput.tsx";
import {LucideSearch} from "lucide-react";
import PluginCard from "@/features/plugins/components/PluginCard.tsx";
import {Separator} from "@/components/ui/separator.tsx";
import TabGroup from "@/components/shared/TabGroup.tsx";

const PluginsPage = () => (
    <>
        <PageHeading heading="Plugin Marketplace"/>

        <Card>
            <CardContent className="p-0">

                <div className="px-4">
                    <IconInput placeholder="Search plugins..." icon={LucideSearch}/>
                </div>

                <Separator className="mt-4"/>

                <div className="px-4 mt-4 rounded-lg flex gap-4 items-center">
                    <span>Filter:</span>
                    <TabGroup items={["All Plugins", "Installed", "Development", "Communication", "Productivity"]}/>
                </div>

                <Separator className="mt-4"/>

                <div className="grid grid-cols-3 gap-4 mt-6 px-4">
                    <PluginCard
                        icon="https://cdn-icons-png.flaticon.com/512/25/25231.png"
                        name="Github"
                        category="Development"
                        version="1.0.0"
                        description="Automate your github workflows with hooks"
                        status="Not Installed"/>
                    <PluginCard
                        icon="https://cdn-icons-png.flaticon.com/512/25/25231.png"
                        name="Github"
                        category="Development"
                        version="1.0.0"
                        description="Automate your github workflows with hooks"
                        status="Installed"/>
                </div>

            </CardContent>
        </Card>
    </>
);

export default PluginsPage;