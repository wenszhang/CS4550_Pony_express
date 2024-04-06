function Button({ className, disabled, children, type = "button", ...rest }) {
    const buttonClassName = [
        className || "",
        "border rounded",
        "px-4 py-2 my-4",
        disabled ?
            "bg-slate-500 italic" :
            "border-green-500 bg-transparent hover:bg-slate-800",
    ].join(" ");

    return (
        <button
            type={type}
            className={buttonClassName}
            disabled={disabled}
            aria-disabled={disabled ? "true" : "false"}
            {...rest}
        >
            {children}
        </button>
    );
}

export default Button;
