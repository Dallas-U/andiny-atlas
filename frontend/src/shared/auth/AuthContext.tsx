import {
    createContext,
    useContext,
    useEffect,
    useState,
    type ReactNode,
} from "react";

import {
    getCurrentUser,
} from "../../features/auth/auth.api";

import type {
    CurrentUser,
} from "../../features/auth/auth.types";

import {
    getStoredAuthToken,
    isAuthenticated as checkIsAuthenticated,
    logout as clearAuthentication,
} from "./auth";

interface AuthContextValue {
    isAuthenticated: boolean;
    currentUser: CurrentUser | null;
    user: CurrentUser | null;
    isLoadingUser: boolean;
    logout: () => void;
    refreshAuthState: () => Promise<void>;
}

const AuthContext = createContext<
    AuthContextValue | undefined
>(undefined);

interface AuthProviderProps {
    children: ReactNode;
}

export function AuthProvider({
    children,
}: AuthProviderProps) {
    const [
        isAuthenticated,
        setIsAuthenticated,
    ] = useState(
        checkIsAuthenticated(),
    );

    const [
        currentUser,
        setCurrentUser,
    ] = useState<CurrentUser | null>(null);

    const [
        isLoadingUser,
        setIsLoadingUser,
    ] = useState(
        checkIsAuthenticated(),
    );

    async function loadCurrentUser(): Promise<void> {
        const token = getStoredAuthToken();

        if (!token) {
            setIsAuthenticated(false);
            setCurrentUser(null);
            setIsLoadingUser(false);
            return;
        }

        setIsAuthenticated(true);
        setIsLoadingUser(true);

        try {
            const user = await getCurrentUser();

            setCurrentUser(user);
        } catch (error) {
            console.error(
                "Failed to load authenticated user:",
                error,
            );

            clearAuthentication();

            setCurrentUser(null);
            setIsAuthenticated(false);
        } finally {
            setIsLoadingUser(false);
        }
    }

    async function refreshAuthState(): Promise<void> {
        await loadCurrentUser();
    }

    function logout(): void {
        clearAuthentication();

        setCurrentUser(null);
        setIsAuthenticated(false);
    }

    useEffect(() => {
        if (checkIsAuthenticated()) {
            void loadCurrentUser();
        } else {
            setIsLoadingUser(false);
        }
    }, []);

    return (
        <AuthContext.Provider
            value={{
                isAuthenticated,
                currentUser,
                user: currentUser,
                isLoadingUser,
                logout,
                refreshAuthState,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth(): AuthContextValue {
    const context = useContext(AuthContext);

    if (!context) {
        throw new Error(
            "useAuth must be used within an AuthProvider.",
        );
    }

    return context;
}