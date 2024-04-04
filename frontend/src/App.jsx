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
import Registration from "./components/Registration.jsx";
import {PrivateRoute} from './utils/PrivateRoute.jsx';
import {PublicRoute} from './utils/PublicRoute.jsx';

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
                                    <PrivateRoute path="/chats">
                                        <Route path="/" element={<SelectChat/>}/>
                                        <Route path="/:chatId" element={<Chats chatId={selectedChatId}/>}/>
                                    </PrivateRoute>
                                    <PrivateRoute path="/profile" element={<Profile/>}/>
                                    <PublicRoute path="/login" element={<Login/>}/>
                                    <PublicRoute path="/register" element={<Registration/>}/>
                                    <Route path="*"
                                           element={isLoggedIn ? <Redirect to="/chats"/> : <Redirect to="/login"/>}/>
                                </Routes>
                            </div>
                        </div>
                    </UserProvider>
                </AuthProvider>
            </BrowserRouter>
        </QueryClientProvider>
    );
}

export default App;