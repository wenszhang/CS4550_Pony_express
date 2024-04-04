import { createContext, useContext, useEffect } from "react";
import { useQuery } from "react-query";
import { useNavigate } from "react-router-dom";
import { useApi, useAuth } from "../hooks";

const User = createContext();

function UserProvider({ children }) {
    const { isLoggedIn, logout, token } = useAuth();
    const navigate = useNavigate();
    const api = useApi();

    const { data } = useQuery({
        queryKey: ["users", token],
        enabled: isLoggedIn,
        staleTime: Infinity,
        queryFn: () => (
            api.get("/users/me")
                .then((response) => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        logout();
                        navigate("/login");
                    }
                })
                .catch((error) => {
                    console.error('Error fetching user data:', error);
                    logout();
                    navigate("/login");
                })
        ),
    });

    return (
        <User.Provider value={data?.user}>
            {children}
        </User.Provider>
    );
}

export { User, UserProvider };