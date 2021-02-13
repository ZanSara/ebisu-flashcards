import {ChangeEvent, FunctionComponent, useState} from "react";

export interface TextFieldProps {
    className?: string;
    placeholder: string;

    validate(value: string): string | null;
}

const TextField: FunctionComponent<TextFieldProps> = (props) => {
    const [initialized, setInitialized] = useState(false);
    const [value, setValue] = useState("");

    const onValueChange = (event: ChangeEvent<HTMLInputElement>) => {
        setValue(event.target.value);
        setInitialized(true);
    }

    const validationClasses = [];
    const validationError = initialized && props.validate(value);
    if (validationError) {
        console.log("Invalid element:", validationError)
        validationClasses.push("placeholder-red-500")
        validationClasses.push("border-red-500")
        validationClasses.push("text-red-500")
    }

    return (
        <div className="flex flex-col border-red-500">
            <input
                className={`text-2xl border-b w-full ${validationClasses.join(' ')}`}
                placeholder={props.placeholder}
                value={value}
                onChange={onValueChange}>
            </input>
            {validationError ? <span className="text-base animate-pulse text-red-500">{validationError}</span> : null}
        </div>
    )
}

export default TextField;