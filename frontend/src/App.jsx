import {QueryClient, QueryClientProvider} from 'react-query';
import {BrowserRouter, Routes, Route, Navigate} from 'react-router-dom';
import {AuthProvider} from "./context/auth";
import {UserProvider} from "./context/user";
import {useAuth} from "./hooks";
import Home from "./components/Home";
import Login from "./components/Login";
import Profile from "./components/Profile";
import Registration from "./components/Registration";
import TopNav from "./components/TopNav";
import Chats from "./components/Chats";
import Chat from "./components/Chat";
import NotFound from "./components/NotFound";

const queryClient = new QueryClient();

function AuthenticatedRoutes() {
    return (
        <Routes>
            <Route path="/" element={<Navigate to="/chats"/>}/>
            <Route path="/chats" element={<Chats/>}>
                <Route path=":chatId" element={<Chat/>}/>
            </Route>
            <Route path="/profile" element={<Profile/>}/>
            <Route path="*" element={<NotFound/>}/>
        </Routes>
    );
}

function UnauthenticatedRoutes() {
    return (
        <Routes>
            <Route path="/login" element={<Login/>}/>
            <Route path="/register" element={<Registration/>}/>
            <Route path="*" element={<Navigate to="/login"/>}/>
        </Routes>
    );
}

function UseRoutes() {
    const { isLoggedIn } = useAuth();
    return (
        <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/register" element={<Registration/>}/>
            <Route path="*" element={isLoggedIn ? <AuthenticatedRoutes/> : <UnauthenticatedRoutes/>}/>
        </Routes>
    );
}

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <AuthProvider>
                <BrowserRouter>
                    <UserProvider>
                        <div className="flex flex-col h-screen bg-gray-700 text-white">
                            <TopNav/>
                            <main className="flex-1 overflow-hidden">
                                <UseRoutes/>
                            </main>
                        </div>
                    </UserProvider>
                </BrowserRouter>
            </AuthProvider>
        </QueryClientProvider>
    );
}

export default App;