import React, {useState} from 'react';
import {QueryClient, QueryClientProvider} from 'react-query';
import {BrowserRouter, Routes, Route, Link} from 'react-router-dom';
import './App.css';
import ChatList from './components/ChatList';
import Chats from './components/Chat';
import SelectChat from './components/SelectChat';
import Login from './components/Login';
import {AuthProvider} from './contexts/auth.jsx';
import {UserProvider} from './contexts/user.jsx';

const queryClient = new QueryClient();

function App() {
    const [selectedChatId, setSelectedChatId] = useState(null);

    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <AuthProvider>
                    <UserProvider>
                        <div className="app-container">
                            <div className="chat-list-column">
                                <ChatList setSelectedChatId={setSelectedChatId}/>
                            </div>
                            <div className="chat-messages-column">
                                <Routes>
                                    <Route path="/" element={<SelectChat/>}/>
                                    <Route path="/chats" element={<SelectChat/>}/>
                                    <Route path="/chats/:chatId" element={<Chats chatId={selectedChatId}/>}/>
                                    <Route path="/login" element={<Login/>}/>
                                </Routes>
                            </div>
                            <Link to="/login" className="login-button">Go to Login</Link>
                        </div>
                    </UserProvider>
                </AuthProvider>
            </BrowserRouter>
        </QueryClientProvider>
    );
}

export default App;