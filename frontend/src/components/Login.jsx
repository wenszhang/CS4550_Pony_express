import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import {useApiWithoutToken, useAuth} from "../hooks.js";
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

function RegistrationLink() {
    return (
        <div className="pt-8 flex flex-col">
            <div className="text-xs">
                need an account?
            </div>
            <Link to="/register">
                <Button className="mt-1 w-full">
                    register
                </Button>
            </Link>
        </div>
    );
}

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const navigate = useNavigate();

    const { login } = useAuth();

    const disabled = username === "" || password === "";

    const api = useApiWithoutToken();

    const onSubmit = (e) => {
        e.preventDefault();

        api.post("/auth/token", { username, password })
            .then(({ access_token }) => {
                login(access_token)
                    .then(() => navigate("/chats"))
                    .catch((error) => {
                        setError('Failed to log in');
                    });
            })
            .catch((error) => {
                setError('Failed to authenticate');
            });
    }

    return (
        <div className="max-w-96 mx-auto py-8 px-4">
            <form onSubmit={onSubmit}>
                <FormInput type="text" name="username" setter={setUsername} />
                <FormInput type="password" name="password" setter={setPassword} />
                <Button className="w-full" type="submit" disabled={disabled}>
                    login
                </Button>
                <Error message={error} />
            </form>
            <RegistrationLink />
        </div>
    );
}

export default Login;