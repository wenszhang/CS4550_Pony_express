import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useApi } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Error({ message }) {
    return message ? (
        <div className="text-red-500 text-xs mt-2">
            {message}
        </div>
    ) : null;
}

function LoginLink() {
    return (
        <div className="pt-8 flex flex-col items-center">
      <span className="text-xs">
        Already have an account?
      </span>
            <Link to="/login">
                <Button className="mt-1 w-full">
                    Login
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
    const [isLoading, setLoading] = useState(false);

    const api = useApi();
    const navigate = useNavigate();

    const disabled = isLoading || !username || !email || !password;

    const onSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const response = await api.post("/auth/registration", { username, email, password });
            if (response.ok) {
                navigate("/login");
            } else {
                const data = await response.json();
                setError(data.detail.error_description || "An error occurred during registration.");
            }
        } catch (error) {
            setError("Network error or server is unreachable.");
        }

        setLoading(false);
    }

    return (
        <div className="max-w-md mx-auto py-8 px-4">
            <form onSubmit={onSubmit} className="space-y-4">
                <FormInput label="Username" type="text" name="username" setter={setUsername} />
                <FormInput label="Email" type="email" name="email" setter={setEmail} />
                <FormInput label="Password" type="password" name="password" setter={setPassword} />
                <Button className="w-full" type="submit" disabled={disabled}>
                    Register
                </Button>
                <Error message={error} />
            </form>
            <LoginLink />
        </div>
    );
}

export default Registration;
