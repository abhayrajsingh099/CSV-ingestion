import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
});

api.interceptors.request.use((config) => {
    const token = JSON.parse(localStorage.getItem("token"))

    if(token && token.access){
        config.headers.Authorization = `Bearer ${token.access}`;
    }

    return config;
});

export default api;