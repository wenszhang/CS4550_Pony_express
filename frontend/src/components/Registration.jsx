import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useApi } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Error({ message }) {
    if (message === "") {
        return <></>;
    }
    return (
        <div className="text-red-300 text-xs">
            {message}
        </div>
    );
}

function LoginLink() {
    return (
        <div className="pt-8 flex flex-col">
            <div className="text-xs">
                already have an account?
            </div>
            <Link to="/login">
                <Button className="mt-1 w-full">
                    login
                </Button>
            </Link>
        </div>
    );
}

function Registration() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const api = useApi();
    const navigate = useNavigate();

    const disabled = username === "" || email === "" || password === "";

    const onSubmit = (e) => {
        e.preventDefault();

        api.post(
            "/auth/registration",
            { username, email, password },
        ).then((response) => {
            navigate("/login");
        }).catch((error) => {
            if (error.body && error.body.detail.type === "duplicate_value") {
                const errorMessage = error.body.detail.entity_field + " already taken";
                setError(errorMessage);
            } else {
                const errorMessage = "error registering";
                setError(errorMessage);
            }
        });
    }

    return (
        <div className="max-w-96 mx-auto py-8 px-4">
            <form onSubmit={onSubmit}>
                <FormInput type="text" name="username" setter={setUsername} />
                <FormInput type="email" name="email" setter={setEmail} />
                <FormInput type="password" name="password" setter={setPassword} />
                <Button className="w-full" type="submit" disabled={disabled}>
                    register
                </Button>
                <Error message={error} />
            </form>
            <LoginLink />
        </div>
    );
}

export default Registration;