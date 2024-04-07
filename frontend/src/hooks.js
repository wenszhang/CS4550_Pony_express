import { useContext } from "react";
import { AuthContext } from "./context/auth";
import { UserContext } from "./context/user";
import api from "./utils/api";

const useApi = () => {
    const { token } = useContext(AuthContext);
    return api(token);
}

const useApiWithoutToken = () => {
    return api();
}

const useAuth = () => useContext(AuthContext);

const useUser = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error("useUser must be used within a UserProvider");
    }
    return context;
}

export {
    useApi,
    useApiWithoutToken,
    useAuth,
    useUser,
};
