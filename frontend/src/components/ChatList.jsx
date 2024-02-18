import React from 'react';
import {useQuery} from 'react-query';
import {Link} from 'react-router-dom';
import axios from 'axios';
import './ChatList.css';

function ChatList() {
    // Access the 'chats' array from the response
    const {data: chats, isLoading, isError, error} = useQuery('chats', () =>
        axios.get('http://localhost:8000/chats').then(res => res.data.chats)
    );

    // Loading state
    if (isLoading) {
        return <div className="chat-list-box">Loading...</div>;
    }

    // Error state
    if (isError) {
        return <div className="chat-list-box">An error has occurred: {error.message}</div>;
    }

    // If messages is an array before rendering
    return (
        <div className="chat-list">
            {Array.isArray(chats) && chats.length > 0 ? (
                chats.map((chat) => (
                    <Link to={`/chats/${chat.id}`} key={chat.id} className="chat-list-box">
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
