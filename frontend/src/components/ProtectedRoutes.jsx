import { Navigate } from "react-router-dom";

function ProtectedRoute({ children }) {

    const token = JSON.parse(localStorage.getItem("token"))

    return (
        <>
            {
                token? children : <Navigate to='/' />
            }
        </>
    )
}

export default ProtectedRoute;