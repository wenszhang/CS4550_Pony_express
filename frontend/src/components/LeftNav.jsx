import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useQuery } from "react-query";
import { useApi } from "../hooks";

function ChatLink({ chat }) {
    const url = `/chats/${chat.id}`;
    const className = ({ isActive }) => [
        "p-2",
        "hover:bg-slate-800 hover:text-white",
        "flex flex-row justify-between",
        isActive ? "bg-slate-800 text-white font-bold" : ""
    ].join(" ");

    const chatName = ({ isActive }) => (
        (isActive ? "\u00bb " : "") + chat.name
    );

    return (
        <NavLink to={url} className={className}>
            {chatName}
        </NavLink>
    );
}

function LeftNav() {
    const [search, setSearch] = useState("");
    const api = useApi();

    const { data, isLoading, isError, error } = useQuery({
        queryKey: ["chats"],
        queryFn: () => (
            api.get("/chats")
                .then((response) => response.json())
        ),
    });

    if (isLoading) {
        return <div className="p-2">Loading chats...</div>;
    }

    if (isError) {
        return <div className="p-2">An error occurred: {error.message}</div>;
    }

    const regex = new RegExp(search.split("").join(".*"), 'i');
    const chats = data?.chats || [];

    const filteredChats = chats.filter(chat => search === "" || regex.test(chat.name));

    return (
        <nav className="flex flex-col border-r-2 border-purple-400 h-main">
            <div className="flex flex-col overflow-y-scroll border-b-2 border-purple-400">
                {filteredChats.map(chat => (
                    <ChatLink key={chat.id} chat={chat} />
                ))}
            </div>
            <div className="p-2">
                <input
                    className="w-full px-4 py-2 bg-gray-700 border border-gray-500"
                    type="search"
                    placeholder="Search chats"
                    onChange={(e) => setSearch(e.target.value)}
                />
            </div>
        </nav>
    );
}

export default LeftNav;
