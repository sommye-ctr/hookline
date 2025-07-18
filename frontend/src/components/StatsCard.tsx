import {Card, CardDescription, CardHeader, CardTitle} from "@/components/ui/card.tsx";

const COLOR_MAP = {
    'chart-1': 'text-[var(--color-chart-1)]',
    'chart-2': 'text-[var(--color-chart-2)]',
    'chart-3': 'text-[var(--color-chart-3)]',
    'chart-4': 'text-[var(--color-chart-4)]',
    'chart-5': 'text-[var(--color-chart-5)]',
}

type StatsProp = {
    title: string,
    description: string,
    color?: keyof typeof COLOR_MAP,
}


const StatsCard = ({title, description, color = "chart-1"}: StatsProp) => {
    const colorClass = COLOR_MAP[color] ?? 'text-muted-foreground';

    return <Card>
        <CardHeader>
            <CardTitle className="flex justify-between">
                {title}
                <h2 className={`${colorClass}`}>12</h2>
            </CardTitle>
            <CardDescription>
                {description}
            </CardDescription>
        </CardHeader>

    </Card>
}

export default StatsCard;