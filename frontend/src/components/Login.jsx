import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useApiWithoutToken, useAuth } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Error({ message }) {
    return message ? (
        <div className="text-red-300 text-xs">
            {message}
        </div>
    ) : null;
}

function RegistrationLink() {
    return (
        <div className="pt-8 flex flex-col">
            <div className="text-xs">
                Need an account?
            </div>
            <Link to="/registration">
                <Button className="mt-1 w-full">
                    Register
                </Button>
            </Link>
        </div>
    );
}

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [isLoading, setLoading] = useState(false);

    const navigate = useNavigate();
    const { login } = useAuth();
    const api = useApiWithoutToken();

    const disabled = isLoading || username === "" || password === "";

    const onSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await api.postForm("/auth/token", { username, password });
            if (response.ok) {
                const userData = await response.json();
                await login(userData);
                navigate("/animals");
            } else {
                const errorData = await response.json();
                setError(errorData.detail.error_description || "Unknown error occurred.");
            }
        } catch (error) {
            setError("Network error or server is unreachable.");
        }

        setLoading(false);
    }

    return (
        <div className="max-w-96 mx-auto py-8 px-4">
            <form onSubmit={onSubmit}>
                <FormInput type="text" name="username" setter={setUsername} />
                <FormInput type="password" name="password" setter={setPassword} />
                <Button className="w-full" type="submit" disabled={disabled}>
                    Login
                </Button>
                <Error message={error} />
            </form>
            <RegistrationLink />
        </div>
    );
}

export default Login;
