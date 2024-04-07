import { createContext, useContext, useState, useEffect } from "react";

const TOKEN_STORAGE_KEY = "__buddy_system_token__";

const getToken = () => sessionStorage.getItem(TOKEN_STORAGE_KEY);
const storeToken = (token) => sessionStorage.setItem(TOKEN_STORAGE_KEY, token);
const clearToken = () => sessionStorage.removeItem(TOKEN_STORAGE_KEY);

const AuthContext = createContext(undefined);

function AuthProvider({ children }) {
    const [token, setToken] = useState(getToken);

    useEffect(() => {
        setToken(getToken());
    }, []);

    const login = (tokenData) => {
        const token = tokenData.access_token;
        setToken(token);
        storeToken(token);
    };

    const logout = () => {
        setToken(null);
        clearToken();
    };

    const isLoggedIn = !!token;

    const contextValue = {
        token,
        isLoggedIn,
        login,
        logout
    };

    return (
        <AuthContext.Provider value={contextValue}>
            {children}
        </AuthContext.Provider>
    );
}

const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
}

export { AuthContext, AuthProvider, useAuth };
