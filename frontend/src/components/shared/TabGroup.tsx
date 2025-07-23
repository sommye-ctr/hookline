import {Button} from "@/components/ui/button.tsx";
import {useState} from "react";

interface TabGroupProps {
    items: string[],
    onSelectedChange?: (index: number) => void,
}

const TabGroup = ({items, onSelectedChange}: TabGroupProps) => {
    const [currentIndex, setCurrentIndex] = useState(0);

    return (
        <>
            <div className="flex items-center gap-4">
                {items.map((item, index) => (
                    <Button
                        className={`rounded-full font-normal ${index == currentIndex ? 'text-white bg-primary' : null}`}
                        variant="secondary"
                        onClick={() => {
                            setCurrentIndex(index);
                            if (onSelectedChange) {
                                onSelectedChange(index);
                            }
                        }}>
                        {item}
                    </Button>
                ))}
            </div>
        </>
    );
}

export default TabGroup;