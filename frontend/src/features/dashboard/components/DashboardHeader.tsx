import { useNavigate } from "@tanstack/react-router";

import { useAuth } from "../../../shared/auth/AuthContext";

function DashboardHeader() {
    const navigate = useNavigate();
    const { logout } = useAuth();

    function handleLogout(): void {
        logout();

        void navigate({
            to: "/",
            replace: true,
        });
    }

    return (
        <header className="flex items-center justify-between border-b border-slate-800 pb-6">
            <div>
                <h1 className="text-3xl font-bold text-white">
                    Andiny Atlas
                </h1>

                <p className="mt-1 text-sm text-slate-400">
                    Investigation Dashboard
                </p>
            </div>

            <button
                type="button"
                onClick={handleLogout}
                className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200 transition hover:border-slate-500 hover:bg-slate-800"
            >
                Sign out
            </button>
        </header>
    );
}

export default DashboardHeader;