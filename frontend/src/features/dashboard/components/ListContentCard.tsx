import {Card, CardContent, CardHeader, CardTitle} from "@/components/ui/card.tsx";
import {Button} from "@/components/ui/button.tsx";
import {LucideArrowRight} from "lucide-react";
import type {JSX} from "react";
import {Separator} from "@/components/ui/separator.tsx";

type Content = {
    title: string,
    value?: string,
    desc: string,
    icon: JSX.Element | string,
}

type ListContentCardProps = {
    title: string,
    actionText: string,
    content: Content[],
    className?: string,
}

const ListContentCard = ({title, actionText, content, className}: ListContentCardProps) => (
    <Card className={className}>
        <CardContent>
            <CardHeader className="px-0 mb-2">
                <div className="flex justify-between items-center">
                    <CardTitle className="p-0">{title}</CardTitle>
                    <Button variant="ghost" className="text-primary">
                        {actionText}
                        <LucideArrowRight/>
                    </Button>
                </div>
            </CardHeader>

            <CardContent className="px-0">
                {
                    content.map((val, _) => {
                            return <div key={val.title + val.value}>
                                <Separator/>
                                <div className="p-4 flex justify-between items-center">

                                    <div className="flex items-center gap-4">
                                        {typeof val.icon === "string" ?
                                            <img className="w-12 h-auto" src={val.icon} alt=""/> : val.icon}
                                        <div className="flex flex-col">
                                            <p className="text-md text-black">{val.title}</p>
                                            <p className="text-sm">{val.desc}</p>
                                        </div>
                                    </div>

                                    {val.value && <div className="text-right">{val.value}</div>}

                                </div>
                            </div>
                        }
                    )
                }
            </CardContent>

        </CardContent>
    </Card>
);

export default ListContentCard;