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

        <div className="flex min-h-screen items-center justify-center bg-muted/30">
            <Card className="w-full max-w-md p-8">
                <form onSubmit={handleLogin}>
                    <Card>
                        <div className="mb-6 text-center">
                            <h1 className="text-3xl font-bold">
                                CSV Dashboard
                            </h1>

                            <p className="text-muted-foreground mt-2">
                                Sign in to manage your CSV documents.
                            </p>
                        </div>

                        <div className="space-y-4">

                            <Input
                                type="email"
                                placeholder="Email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                            />

                            <Input
                                type="password"
                                placeholder="Password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                            />

                        </div>
                        {
                            error && (
                                <p className="mt-4 text-sm text-red-500">
                                    {error}
                                </p>
                            )
                        }


                        <Button
                            className="mt-6 w-full"
                            type="submit"
                            disabled={loading}
                        >
                            {loading ? "Signing in..." : "Sign In"}
                        </Button>

                    </Card>
                </form>
            </Card>
        </div>


    )
}

export default Login;