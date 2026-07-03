import { useNavigate } from "react-router-dom";
import { Button } from "./ui/button";

function Navbar() {
    const navigate = useNavigate();

    function handleLogout() {
        localStorage.removeItem("token");
        navigate('/')
    }

    return (
        <>
            <h1>CSV DASHBOARD</h1>

            <Button onClick={handleLogout}>
                Logout
            </Button>
        </>
    )
}

export default Navbar;