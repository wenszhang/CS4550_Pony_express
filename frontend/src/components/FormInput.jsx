function FormInput({ setter, ...props }) {
    let onChange;
    if (props.onChange) {
        onChange = props.onChange;
    } else if (setter) {
        onChange = (e) => setter(e.target.value);
    } else {
        onChange = () => {};
    }

    const className = [
        props.className || "",
        "border rounded",
        "px-4 py-2",
        props.readOnly ?
            "bg-slate-500" :
            "bg-transparent border-lgrn",
    ].join(" ");

    return (
        <div className="flex flex-col py-2">
            <label htmlFor={props.name}>{props.name}</label>
            <input
                {...props}
                className={className}
                onChange={onChange}
            />
        </div>
    );
}

export default FormInput;
