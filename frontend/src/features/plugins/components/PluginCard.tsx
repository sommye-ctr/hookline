import {Card, CardContent, CardFooter, CardHeader} from "@/components/ui/card.tsx";
import {Badge} from "@/components/ui/badge.tsx";
import {Button} from "@/components/ui/button.tsx";

interface PluginCardProps {
    icon: string,
    name: string,
    category: string,
    version: string,
    description: string,
    status: 'Installed' | 'Not Installed',
}

const PluginCard = ({icon, name, category, version, description, status}: PluginCardProps) => (
    <Card className="pb-0 hover:shadow-md">
        <CardHeader className="flex gap-4 items-center">
            <img className="w-10 h-auto" src={icon} alt=""/>
            <div className="flex flex-col">
                <h4 className="text-black">{name}</h4>
                <p className="text-xs">{category} • v{version}</p>
            </div>
        </CardHeader>

        <CardContent>
            <p className="text-sm">{description}</p>
        </CardContent>

        <CardFooter className="bg-muted flex justify-between p-2 items-center">
            {status === 'Installed'
                ? <Badge className="bg-green-500">{status}</Badge>
                : <span className="text-sm">Not Installed</span>}

            <Button variant="ghost" className="text-primary">
                {status === 'Installed' ? 'Configure' : 'Install'}
            </Button>
        </CardFooter>
    </Card>
);

export default PluginCard;