import { useEffect, useState } from "react";

import { getCurrentUser } from "../../auth/auth.api";
import type { UserResponse } from "../../auth/user.types";

function WelcomeCard() {
    const [user, setUser] = useState<UserResponse | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [errorMessage, setErrorMessage] = useState<string | null>(null);

    useEffect(() => {
        async function loadCurrentUser(): Promise<void> {
            try {
                const currentUser = await getCurrentUser();

                setUser(currentUser);
            } catch (error) {
                console.error("Failed to load current user:", error);
                setErrorMessage("Unable to load your profile.");
            } finally {
                setIsLoading(false);
            }
        }

        void loadCurrentUser();
    }, []);

    if (isLoading) {
        return (
            <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
                <p className="text-slate-400">Loading your profile...</p>
            </section>
        );
    }

    if (errorMessage || !user) {
        return (
            <section className="mt-8 rounded-xl border border-red-900 bg-slate-900 p-6">
                <p className="text-red-400">
                    {errorMessage ?? "Unable to load your profile."}
                </p>
            </section>
        );
    }

    return (
        <section className="mt-8 rounded-xl border border-slate-800 bg-slate-900 p-6">
            <p className="text-sm font-medium uppercase tracking-wide text-slate-500">
                Welcome back
            </p>

            <h2 className="mt-2 text-2xl font-semibold text-white">
                {user.full_name}
            </h2>

            <div className="mt-6 grid gap-4 sm:grid-cols-2">
                <div>
                    <p className="text-sm text-slate-500">Email</p>
                    <p className="mt-1 text-slate-200">{user.email}</p>
                </div>

                <div>
                    <p className="text-sm text-slate-500">Account status</p>
                    <p className="mt-1 text-slate-200">
                        {user.is_active ? "Active" : "Inactive"}
                    </p>
                </div>
            </div>
        </section>
    );
}

export default WelcomeCard;