import React from 'react';
import { useAuth } from '../hooks';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="flex flex-col items-center justify-center space-y-4">
            <div className="text-xl">username: {user.username}</div>
            <div className="text-xl">email: {user.email}</div>
            <div className="text-xl">member since: {new Date(user.created_at).toDateString()}</div>
            <button
                className="px-4 py-2 bg-blue-500 text-white rounded"
                onClick={handleLogout}
            >
                logout
            </button>
        </div>
    );
};

export default Profile;