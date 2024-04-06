import { NavLink } from "react-router-dom";
import { useAuth, useUser } from "../hooks";

function NavItem({ to, name, right }) {
    const className = [
        "border-purple-400",
        "py-2 px-4",
        "hover:bg-slate-800",
        right ? "ml-auto border-l-2" : "border-r-2"
    ].join(" ");

    const getClassName = ({ isActive }) => (
        isActive ? `${className} bg-slate-800` : className
    );

    return (
        <NavLink to={to} className={getClassName}>
            {name}
        </NavLink>
    );
}

function AuthenticatedNavItems() {
    const { user } = useUser();

    return (
        <>
            <NavItem to="/" name="pony express" />
            <NavItem to="/chats" name="chats" />
            <NavItem to="/profile" name={user?.username || 'Profile'} right />
        </>
    );
}

function UnauthenticatedNavItems() {
    return (
        <>
            <NavItem to="/" name="pony express" />
            <div className="flex-1" />
            <NavItem to="/login" name="login" right />
        </>
    );
}

function TopNav() {
    const { isLoggedIn } = useAuth();

    return (
        <nav className="flex flex-row items-center border-b-4 border-purple-400">
            {isLoggedIn ? <AuthenticatedNavItems /> : <UnauthenticatedNavItems />}
        </nav>
    );
}

export default TopNav;
