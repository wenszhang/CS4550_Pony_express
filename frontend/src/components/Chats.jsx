import React, { useRef, useCallback } from 'react';
import LeftNav from "./LeftNav";
import { Outlet } from "react-router-dom";

function Chats() {
    const leftNavRef = useRef(null);

    const onMouseDown = useCallback((e) => {
        document.onmousemove = onMouseMove;
        document.onmouseup = () => {
            document.onmousemove = document.onmouseup = null;
        };

        function onMouseMove(e) {
            const newWidth = e.clientX;
            leftNavRef.current.style.width = `${newWidth}px`;
        }

        e.preventDefault();
    }, []);

    return (
        <div className="flex flex-row h-full">
            <div ref={leftNavRef} className="bg-gray-800 border-r" style={{ width: '20%' }}>
                <LeftNav />
            </div>
            <div
                className="cursor-col-resize"
                style={{ background: '#343a40', width: '0.5rem' }}
                onMouseDown={onMouseDown}
            />
            <div className="flex-1">
                <Outlet />
            </div>
        </div>
    );
}

export default Chats;
