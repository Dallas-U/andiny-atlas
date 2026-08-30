const ACCESS_TOKEN_KEY = "andiny_atlas_access_token";
const TOKEN_TYPE_KEY = "andiny_atlas_token_type";

export interface StoredToken {
    access_token: string;
    token_type: string;
}

export function saveToken(token: StoredToken): void {
    sessionStorage.setItem(ACCESS_TOKEN_KEY, token.access_token);
    sessionStorage.setItem(TOKEN_TYPE_KEY, token.token_type);
}

export function getToken(): StoredToken | null {
    const accessToken = sessionStorage.getItem(ACCESS_TOKEN_KEY);
    const tokenType = sessionStorage.getItem(TOKEN_TYPE_KEY);

    if (!accessToken || !tokenType) {
        return null;
    }

    return {
        access_token: accessToken,
        token_type: tokenType,
    };
}

export function removeToken(): void {
    sessionStorage.removeItem(ACCESS_TOKEN_KEY);
    sessionStorage.removeItem(TOKEN_TYPE_KEY);
}