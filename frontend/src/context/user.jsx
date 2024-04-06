import { createContext, useContext, useEffect } from "react";
import { useQuery } from "react-query";
import { useNavigate } from "react-router-dom";
import { useApi, useAuth } from "../hooks";

const UserContext = createContext();

function UserProvider({ children }) {
    const { isLoggedIn, logout, token } = useAuth();
    const navigate = useNavigate();
    const api = useApi();

    const fetchUserData = async () => {
        try {
            const response = await api.get("/users/me");
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to fetch user data.');
            }
        } catch (error) {
            // Logout the user and navigate to login if there's an error fetching user data
            logout();
            navigate("/login");
            // It could be beneficial to handle errors more granularly, depending on your app's needs
        }
    };

    const { data, error } = useQuery(["users", token], fetchUserData, {
        enabled: isLoggedIn && !!token,
        staleTime: Infinity, // Use appropriate stale time as needed
        cacheTime: 0, // Avoid caching this data if it should always be fresh on reload
        onError: (err) => {
            // Optional: handle errors in a centralized error handling logic here
            console.error("Error fetching user data:", err);
        }
    });

    useEffect(() => {
        if (!isLoggedIn) {
            navigate("/login");
        }
    }, [isLoggedIn, navigate]);

    return (
        <UserContext.Provider value={data?.user || null}>
            {children}
        </UserContext.Provider>
    );
}

// Custom hook to use the UserContext
const useUser = () => {
    const context = useContext(UserContext);
    if (context === undefined) {
        throw new Error('useUser must be used within a UserProvider');
    }
    return context;
}

export { UserContext, UserProvider, useUser };
