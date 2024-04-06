import { useNavigate } from 'react-router-dom';
import { useAuth } from '../hooks';

const PrivateRoute = ({ children }) => {
    const { isLoggedIn } = useAuth();
    const navigate = useNavigate();

    if (!isLoggedIn) {
        navigate('/login');
        return null;
    }

    return children;
};

export default PrivateRoute;