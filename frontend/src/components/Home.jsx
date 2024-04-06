import React from 'react';
import {useAuth} from '../hooks';
import {Link} from 'react-router-dom';

function HomePage() {
    const {isLoggedIn} = useAuth();

    return (
        <div className="home-page">
            <h1>Welcome to Our Application!</h1>
            {isLoggedIn ? (
                <p>You are logged in! Navigate to <Link to="/chats">Chats</Link> or <Link to="/profile">Your
                    Profile</Link>.</p>
            ) : (
                <p>
                    Please <Link to="/login">Log In</Link> or <Link to="/register">Register</Link> to continue.
                </p>
            )}
        </div>
    );
}

export default HomePage;
