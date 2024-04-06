import { useState } from "react";
import { NavLink } from "react-router-dom";
import { useQuery } from "react-query";
import { useApi } from "../hooks";

function ChatLink({ chat }) {
    const url = `/chats/${chat.id}`;
    const className = ({ isActive }) => [
        "p-2",
        "hover:bg-slate-500 hover:text-white",
        "flex flex-row justify-between",
        isActive ? "bg-slate-600 text-white font-bold" : ""
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
            api.get("/chats").then((response) => response.json())
        ),
    });

    if (isLoading) {
        return <div className="p-2 text-white">Loading chats...</div>;
    }

    if (isError) {
        return <div className="p-2 text-red-500">An error occurred: {error.message}</div>;
    }

    const regex = new RegExp(search.split("").join(".*"), 'i');
    const chats = data?.chats || [];

    const filteredChats = chats.filter(chat => search === "" || regex.test(chat.name));

    return (
        <nav className="flex flex-col w-full border-r border-gray-700 bg-gray-800 text-white">
            <div className="p-2">
                <input
                    className="w-full px-4 py-2 mb-2 bg-gray-700 border border-gray-600 placeholder-gray-400 text-white"
                    type="search"
                    placeholder="Search chats"
                    onChange={(e) => setSearch(e.target.value)}
                />
            </div>
            <div className="flex-1 overflow-y-auto">
                {filteredChats.map(chat => (
                    <ChatLink key={chat.id} chat={chat} />
                ))}
            </div>
        </nav>
    );
}

export default LeftNav;