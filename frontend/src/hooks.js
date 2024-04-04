import { useContext } from "react";
import { Auth as AuthContext } from "./contexts/auth";
import { User as UserContext } from "./contexts/user";
import api from "./utils/api";

const useApi = () => {
    const { token } = useAuth();
    return api(token);
}
const useApiWithoutToken = () => {
    return api();
}

const useAuth = () => useContext(AuthContext);

const useUser = () => useContext(UserContext);

export {
    useApi,
    useApiWithoutToken,
    useAuth,
    useUser,
};