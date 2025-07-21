import PageHeading from "@/components/shared/PageHeading.tsx";
import {Card, CardContent} from "@/components/ui/card.tsx";
import IconInput from "@/components/shared/IconInput.tsx";
import {LucideSearch} from "lucide-react";

const PluginsPage = () => (
    <>
        <PageHeading heading="Plugin Marketplace"/>

        <Card>
            <CardContent>

                <IconInput placeholder="Search plugins..." icon={LucideSearch}/>

            </CardContent>
        </Card>
    </>
);

export default PluginsPage;