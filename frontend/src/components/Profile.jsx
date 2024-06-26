import { useEffect, useState } from "react";
import { useAuth, useUser, useApi } from "../hooks";
import Button from "./Button";
import FormInput from "./FormInput";

function Profile() {
    const { logout } = useAuth();
    const { user, isLoading } = useUser();
    const api = useApi();
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [createdDate, setCreatedDate] = useState("");
    const [isEditing, setIsEditing] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (user) {
            setUsername(user.username || '');
            setEmail(user.email || '');
            setCreatedDate(new Date(user.created_at).toDateString());
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

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.put("/users/me", { username, email });
            if (!response.ok) {
                setError('Failed to update profile');
            }
            alert("Profile updated successfully!");
            setIsEditing(false);
        } catch (err) {
            setError(err.message || "An error occurred while updating the profile.");
            console.error("Profile update error:", err);
        }
    };

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="max-w-md mx-auto p-4">
            <h2 className="text-2xl font-bold py-2">Profile Details</h2>
            {error && <div className="text-red-500 text-sm mb-2">{error}</div>}
            <form className="border rounded px-4 py-4" onSubmit={handleSubmit}>
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
                <div className="py-2">
                    <label className="block text-sm font-medium">Member Since:</label>
                    <div className="mt-1">
                        {createdDate}
                    </div>
                </div>
                {isEditing ? (
                    <>
                        <Button type="submit" className="mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                            Update
                        </Button>
                        <Button type="button" onClick={handleCancel} className="mt-4 ml-4 bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
                            Cancel
                        </Button>
                    </>
                ) : (
                    <Button type="button" onClick={handleEdit} className="mt-4 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
                        Edit
                    </Button>
                )}
            </form>
            <Button onClick={logout} className="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
                Logout
            </Button>
        </div>
    );
}

export default Profile;
