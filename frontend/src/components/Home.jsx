import React from 'react';
import {useAuth} from '../hooks';
import {Link} from 'react-router-dom';

function HomePage() {
    const {isLoggedIn} = useAuth();

    return (
        <div className="home-page container mx-auto text-center py-20">
            <h1 className="text-4xl mb-8">Welcome to Pony Express!</h1>
            {isLoggedIn ? (
                <p className="text-xl">
                    You are logged in! Navigate to <Link className="text-blue-500" to="/chats">Chats</Link> or <Link className="text-blue-500" to="/profile">Your Profile</Link>.
                </p>
            ) : (
                <p className="text-xl">
                    Please <Link className="text-blue-500" to="/login">Log In</Link> or <Link className="text-blue-500" to="/register">Register</Link> to continue.
                </p>
            )}
        </div>
    );
}

export default HomePage;