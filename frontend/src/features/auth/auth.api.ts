import { apiClient } from "../../shared/api/client";

import type {
    CurrentUser,
    LoginRequest,
    Token,
} from "./auth.types";

export async function login(
    request: LoginRequest,
): Promise<Token> {
    const response = await apiClient.post<Token>(
        "/auth/login",
        request,
    );

    return response.data;
}

export async function getCurrentUser(): Promise<CurrentUser> {
    const response = await apiClient.get<CurrentUser>(
        "/auth/me",
    );

    return response.data;
}