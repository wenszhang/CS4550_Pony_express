import {Redirect, Route} from 'react-router-dom';
import {useContext} from 'react';
import {Auth} from '../contexts/auth.jsx';

export function PrivateRoute({children, ...rest}) {
    const {isLoggedIn} = useContext(Auth);
    return (
        <Route
            {...rest}
            render={({location}) =>
                isLoggedIn ? (
                    children
                ) : (
                    <Redirect
                        to={{
                            pathname: "/login",
                            state: {from: location}
                        }}
                    />
                )
            }
        />
    );
}