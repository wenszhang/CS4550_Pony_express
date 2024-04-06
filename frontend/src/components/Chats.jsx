import Chat from "./Chat";
import LeftNav from "./LeftNav";

function Chats() {
    return (
        <div className="flex flex-row h-main">
            <div className="w-40 bg-gray-200">
                <LeftNav />
            </div>
            <div className="flex-1 p-8">
                <Chat />
            </div>
        </div>
    );
}

export default Chats;
