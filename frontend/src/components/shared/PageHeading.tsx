import {Button} from "@/components/ui/button.tsx";
import type {JSX} from "react";

type PageHeadingProps = {
    heading: string,
    buttonIcon: JSX.Element,
    buttonText: string,
}

const PageHeading = ({heading, buttonIcon, buttonText}: PageHeadingProps) => (
    <div className="flex justify-between my-7">
        <h3>{heading}</h3>
        <Button>
            {buttonIcon}
            {buttonText}
        </Button>
    </div>
);

export default PageHeading;