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
            <header className="border-b">
                <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">

                    <h1 className="text-xl font-bold">
                        CSV Dashboard
                    </h1>

                    <Button
                        variant="outline"
                        onClick={handleLogout}
                    >
                        Logout
                    </Button>

                </div>
            </header>
        </>
    )
}

export default Navbar;