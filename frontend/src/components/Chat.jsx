import { useQuery } from "react-query";
import { useParams } from "react-router-dom";
import { useApi } from "../hooks";

function Message({ message }) {
    const className = "flex flex-col p-2 border-b border-slate-300";

    const formatDate = (date) => {
        return `${new Date(date).toDateString()} - ${new Date(date).toLocaleTimeString()}`;
    }

    return (
        <div className={className}>
            <div className="font-bold">{message.user_id}</div>
            <div className="text-sm text-slate-500">{formatDate(message.created_at)}</div>
            <div>{message.text}</div>
        </div>
    );
}

function NoMessages() {
    return (
        <div className="font-bold text-2xl py-4 text-center">
            No messages or still loading...
        </div>
    );
}

function ChatMessages({ messages }) {
    if (messages && messages.length > 0) {
        return (
            <div className="flex flex-col p-4">
                {messages.map((message) => (
                    <Message key={message.id} message={message} />
                ))}
            </div>
        );
    }

    return <NoMessages />;
}

function Chat() {
    const { chatId } = useParams();
    const api = useApi();

    const { data, isLoading, isError, error } = useQuery({
        queryKey: ["chats", chatId, "messages"],
        queryFn: () => (
            api.get(`/chats/${chatId}/messages`)
                .then((response) => response.json())
        ),
        enabled: !!chatId,
    });

    if (isLoading) {
        return <div className="text-center text-xl">Loading...</div>;
    }

    if (isError) {
        return <div className="text-center text-xl text-red-500">An error occurred: {error.message}</div>;
    }

    return <ChatMessages messages={data?.messages} />;
}

export default Chat;