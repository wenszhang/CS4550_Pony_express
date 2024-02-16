import React from 'react';
import { useQuery } from 'react-query';
import { Link } from 'react-router-dom';
import axios from 'axios';

function ChatList() {
    // Fetch chats
    const { data: chats, isLoading, isError, error } = useQuery('chats', () =>
        axios.get('http://localhost:8000/chats').then(res => res.data.chats) // Access the 'chats' array from the response
    );

    // Display loading state
    if (isLoading) {
        return <div>Loading...</div>;
    }

    // Display error state
    if (isError) {
        return <div>An error has occurred: {error.message}</div>;
    }

    // If messages is an array before rendering
    return (
        <div className="chat-list">
            {Array.isArray(chats) && chats.length > 0 ? (
                chats.map((chat) => (
                    <Link to={`/chats/${chat.id}`} key={chat.id} className="chat-box">
                        <div className="chat-name">{chat.name}</div>
                        <div className="chat-users">{chat.user_ids.join(', ')}</div>
                        <div className="chat-created">Created at: {new Date(chat.created_at).toDateString()}</div>
                    </Link>
                ))
            ) : (
                <div>No chats available or still loading...</div>
            )}
        </div>
    );
}

export default ChatList;
