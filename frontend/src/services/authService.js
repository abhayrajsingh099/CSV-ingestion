import axios from "axios";

const authApi = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
});

export async function login(username, password) {
    const response = await authApi.post('/token/', {
        username,
        password,
    });

    return response.data
}