import { createContext, useContext, useEffect } from "react";
import { useQuery } from "react-query";
import { useNavigate } from "react-router-dom";
import { useApi, useAuth } from "../hooks";

const UserContext = createContext({ user: null, isLoading: true, isError: false });

function UserProvider({ children }) {
    const { isLoggedIn, logout, token } = useAuth();
    const navigate = useNavigate();
    const api = useApi();

    const { data, error, isLoading } = useQuery(["users", token], () => api.get("/users/me").then(res => res.json()), {
        enabled: isLoggedIn && !!token,
        staleTime: Infinity,
        cacheTime: 0,
        onError: (err) => {
            console.error("Error fetching user data:", err);
            logout();
            navigate("/login");
        }
    });

    useEffect(() => {
        if (!isLoggedIn && !isLoading) {
            navigate("/login");
        }
    }, [isLoggedIn, isLoading, navigate]);

    return (
        <UserContext.Provider value={{ user: data?.user, isLoading, isError: !!error }}>
            {children}
        </UserContext.Provider>
    );
}

const useUser = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within a UserProvider');
    }
    return context;
}

export { UserContext, UserProvider, useUser };
