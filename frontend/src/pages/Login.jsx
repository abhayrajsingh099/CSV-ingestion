import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useState } from "react"

function Login() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    return (
        <div >
            <Card>
                <h1 color="green">CSV DASHBOARD</h1>

                <Input
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    placeholder="Enter username .."
                />

                <Input
                    type="text"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Enter password .."
                />

                <Button onClick={"dd"}>
                    Login
                </Button>

            </Card>
        </div>

    )
}

export default Login;