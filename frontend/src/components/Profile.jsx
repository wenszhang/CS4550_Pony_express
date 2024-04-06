import { useEffect, useState } from "react";
import { useAuth, useUser } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
    const { logout } = useAuth();
    const user = useUser();
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        if (user) {
            setUsername(user.username);
            setEmail(user.email);
        }
    }, [user]);

    const handleEdit = () => {
        setIsEditing(true);
    };

    const handleCancel = () => {
        setIsEditing(false);
        setUsername(user.username);
        setEmail(user.email);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Updated Username:", username);
        console.log("Updated Email:", email);
        setIsEditing(false);
    };

    return (
        <div className="max-w-96 mx-auto px-4 py-8">
            <h2 className="text-2xl font-bold py-2">
                Details
            </h2>
            <form className="border rounded px-4 py-2" onSubmit={handleSubmit}>
                <FormInput
                    label="Username"
                    name="username"
                    type="text"
                    value={username}
                    readOnly={!isEditing}
                    setter={setUsername}
                />
                <FormInput
                    label="Email"
                    name="email"
                    type="email"
                    value={email}
                    readOnly={!isEditing}
                    setter={setEmail}
                />
                {isEditing ? (
                    <>
                        <Button type="submit" className="mr-8">
                            Update
                        </Button>
                        <Button type="button" onClick={handleCancel}>
                            Cancel
                        </Button>
                    </>
                ) : (
                    <Button type="button" onClick={handleEdit}>
                        Edit
                    </Button>
                )}
            </form>
            <Button onClick={logout}>
                Logout
            </Button>
        </div>
    );
}

export default Profile;
