import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useState } from "react"

import { login } from "@/services/authService";
import { useNavigate } from "react-router-dom";

function Login() {
    const navigate = useNavigate();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleLogin(e) {
        e.preventDefault();

        setError("");
        setLoading(true);

        try {
            const data = await login(email, password);
            localStorage.setItem("token", JSON.stringify(data))
            navigate("/dashboard");
        } catch(e) {
            setError(e.message);
        } finally {
            setLoading(false);
        }

    }

    return (
        <form onSubmit={handleLogin}>
            <Card>
                <h1 color="green">CSV DASHBOARD</h1>

                <Input
                    type="text"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Enter email .."
                />

                <Input
                    type="text"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter password .."
                />

                {
                    <p>{error && true}</p>
                }


                <Button
                    type="submit"
                    disabled={loading}>
                    {loading? "login..." : "Login"}
                </Button>

            </Card>
        </form>

    )
}

export default Login;