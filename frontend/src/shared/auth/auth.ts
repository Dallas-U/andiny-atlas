import {
    getToken,
    removeToken,
    type StoredToken,
} from "./tokenStorage";

export function getStoredAuthToken(): StoredToken | null {
    return getToken();
}

export function isAuthenticated(): boolean {
    return getToken() !== null;
}

export function logout(): void {
    removeToken();
}