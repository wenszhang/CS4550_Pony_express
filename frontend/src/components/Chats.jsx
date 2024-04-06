import LeftNav from "./LeftNav";
import {Outlet} from "react-router-dom";

function Chats() {
    return (
        <div className="flex flex-row min-h-screen">
            <div className="w-40 bg-gray-200 border-r">
                <LeftNav />
            </div>
            <div className="flex-1 p-8 overflow-hidden">
                <Outlet />
            </div>
        </div>
    );
}

export default Chats;
