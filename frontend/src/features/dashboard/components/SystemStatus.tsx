import { CheckCircle2 } from "lucide-react";
import { useTranslation } from "react-i18next";

import { useAuth } from "../../../shared/auth/AuthContext";
import Card from "../../../shared/components/Card";

function SystemStatus() {
    const { user } = useAuth();
    const { t } = useTranslation();

    function getRoleLabel(
        role: string | undefined,
    ): string {
        switch (role) {
            case "super_admin":
                return t("roles.superAdmin");

            case "admin":
                return t("roles.admin");

            case "supervisor":
                return t("roles.supervisor");

            case "agent":
                return t("roles.agent");

            default:
                return t("roles.unknown");
        }
    }

    const statusItems = [
        {
            label: t("dashboard.systemStatus.authentication"),
            value: t(
                "dashboard.systemStatus.authenticated",
            ),
        },
        {
            label: t("dashboard.systemStatus.currentRole"),
            value: getRoleLabel(user?.role),
        },
        {
            label: t("dashboard.systemStatus.environment"),
            value: import.meta.env.DEV
                ? t(
                    "dashboard.systemStatus.development",
                )
                : t(
                    "dashboard.systemStatus.production",
                ),
        },
    ];

    return (
        <section className="mt-10 mb-12">
            <div>
                <h2 className="text-xl font-semibold text-white">
                    {t("dashboard.systemStatus.title")}
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    {t("dashboard.systemStatus.subtitle")}
                </p>
            </div>

            <Card className="mt-4 divide-y divide-slate-800 p-0">
                {statusItems.map((item) => (
                    <div
                        key={item.label}
                        className="flex items-center justify-between px-6 py-4"
                    >
                        <div className="flex items-center gap-3">
                            <CheckCircle2 className="h-5 w-5 text-green-400" />

                            <span className="text-slate-300">
                                {item.label}
                            </span>
                        </div>

                        <span className="rounded-full bg-green-900/40 px-3 py-1 text-sm font-medium text-green-300">
                            {item.value}
                        </span>
                    </div>
                ))}
            </Card>
        </section>
    );
}

export default SystemStatus;