import {Input} from "@/components/ui/input.tsx";
import * as React from "react";
import {type ChangeEvent} from "react";

interface IconInputProps {
    placeholder: string,
    onChange?: (value: ChangeEvent<HTMLInputElement>) => void,
    icon: React.ElementType,
}

const IconInput = ({placeholder, onChange, icon: Icon}: IconInputProps) => (
    <div className="relative w-full">
        <Input
            className="pl-8"
            placeholder={placeholder}
            onChange={onChange}
        />
        <Icon className="absolute top-1/2 left-2 size-4 -translate-y-1/2 opacity-50 select-none"/>
    </div>
);

export default IconInput;