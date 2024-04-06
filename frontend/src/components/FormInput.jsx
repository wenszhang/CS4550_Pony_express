function FormInput({ setter, ...props }) {
    const onChange = props.onChange || (setter ? (e) => setter(e.target.value) : undefined);

    const inputClassName = [
        "border rounded px-4 py-2",
        props.className || "",
        props.readOnly ? "bg-slate-500" : "bg-transparent border-green-500"
    ].join(" ");

    return (
        <div className="flex flex-col py-2">
            <label htmlFor={props.name} className="capitalize">
                {props.label || props.name}
            </label>
            <input
                {...props}
                className={inputClassName}
                onChange={onChange}
                id={props.name}
            />
        </div>
    );
}

export default FormInput;
