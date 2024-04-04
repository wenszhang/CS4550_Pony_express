function Button(props) {
    const className = [
        props.className || "",
        "border rounded",
        "px-4 py-2 my-4",
        props.disabled ?
            "bg-slate-500 italic" :
            "border-lgrn bg-transparent hover:bg-slate-800",
    ].join(" ");

    return (
        <button {...props} className={className}>
            {props.children}
        </button>
    );
}

export default Button;