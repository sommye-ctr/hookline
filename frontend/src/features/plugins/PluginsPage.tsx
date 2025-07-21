import PageHeading from "@/components/shared/PageHeading.tsx";
import {Card, CardContent} from "@/components/ui/card.tsx";
import IconInput from "@/components/shared/IconInput.tsx";
import {LucideSearch} from "lucide-react";
import PluginCard from "@/features/plugins/components/PluginCard.tsx";

const PluginsPage = () => (
    <>
        <PageHeading heading="Plugin Marketplace"/>

        <Card>
            <CardContent>

                <IconInput placeholder="Search plugins..." icon={LucideSearch}/>

                <div className="grid grid-cols-3 gap-4 mt-8">
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