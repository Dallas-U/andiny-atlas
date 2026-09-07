import { useNavigate } from "@tanstack/react-router";
import { useTranslation } from "react-i18next";

import { useAuth } from "../../../shared/auth/AuthContext";
import LanguageSelector from "../../../shared/i18n/LanguageSelector";

function DashboardHeader() {
    const navigate = useNavigate();
    const { logout } = useAuth();
    const { t } = useTranslation();

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
                    {t("dashboard.title")}
                </h1>

                <p className="mt-1 text-sm text-slate-400">
                    {t("dashboard.subtitle")}
                </p>
            </div>

            <div className="flex items-center gap-3">
                <LanguageSelector />

                <button
                    type="button"
                    onClick={handleLogout}
                    className="rounded-lg border border-slate-700 px-4 py-2 text-sm font-medium text-slate-200 transition hover:border-slate-500 hover:bg-slate-800"
                >
                    {t("auth.signOut")}
                </button>
            </div>
        </header>
    );
}

export default DashboardHeader;