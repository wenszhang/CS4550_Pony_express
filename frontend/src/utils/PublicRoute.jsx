import {Redirect, Route} from "react-router-dom";
import {useContext} from "react";
import {Auth} from "../contexts/auth.jsx";

export function PublicRoute({children, ...rest}) {
    const {isLoggedIn} = useContext(Auth);
    return (
        <Route
            {...rest}
            render={({location}) =>
                !isLoggedIn ? (
                    children
                ) : (
                    <Redirect
                        to={{
                            pathname: "/chats",
                            state: {from: location}
                        }}
                    />
                )
            }
        />
    );
}