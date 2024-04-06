import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks'; // import useAuth from hooks.js

const PublicRoute = ({ children }) => {
    const { isLoggedIn } = useAuth(); // use useAuth hook
    const navigate = useNavigate();

    if (isLoggedIn) {
        navigate('/chats');
        return null;
    }

    return children;
};

export default PublicRoute;