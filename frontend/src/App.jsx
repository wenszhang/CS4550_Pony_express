import { QueryClient, QueryClientProvider } from 'react-query';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import './App.css';
import ChatList from './components/ChatList';
import Chats from './components/Chat';
import SelectChat from './components/SelectChat';

const queryClient = new QueryClient();

function App() {
    const [selectedChatId, setSelectedChatId] = useState(null);

    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <div className="app-container">
                    <div className="left-column">
                        <ChatList setSelectedChatId={setSelectedChatId}/>
                    </div>
                    <div className="right-column">
                        <Routes>
                            <Route path="/" element={<SelectChat/>}/>
                            <Route path="/chats" element={<SelectChat/>}/>
                            <Route path="/chats/:chatId" element={<Chats chatId={selectedChatId}/>}/>
                        </Routes>
                    </div>
                </div>
            </BrowserRouter>
        </QueryClientProvider>
    );
}

export default App;