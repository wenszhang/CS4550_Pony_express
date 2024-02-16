import React from 'react';
import { useQuery } from 'react-query';
import { useParams } from 'react-router-dom';
import axios from 'axios';

function Chat() {
    const { chatId } = useParams(); // get chatId from the URL parameters

    // Fetch messages specific chat
    const { data, isLoading, error } = useQuery(['messages', chatId], () =>
        axios.get(`http://localhost:8000/chats/${chatId}/messages`).then(res => res.data)
    );

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>An error has occurred: {error.message}</div>;

    // If messages is an array before rendering
    return (
        <div className="messages-list">
            {Array.isArray(data?.messages) ? (
                data.messages.map((message) => (
                    <div key={message.id} className="message-box">
                        <div>{message.user_id} {new Date(message.created_at).toDateString()} - {new Date(message.created_at).toLocaleTimeString()}</div>
                        <div>{message.text}</div>
                    </div>
                ))
            ) : (
                <p>No messages or still loading...</p>
            )}
        </div>
    );
}

export default Chat;
