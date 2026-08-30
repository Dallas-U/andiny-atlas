import axios from "axios";

import { getToken } from "../auth/tokenStorage";

export const apiClient = axios.create({
    baseURL: "http://127.0.0.1:8000",
    headers: {
        "Content-Type": "application/json",
    },
});

apiClient.interceptors.request.use((config) => {
    const token = getToken();

    if (token) {
        config.headers.Authorization =
            `${token.token_type} ${token.access_token}`;
    }

    return config;
});