import {
    BarChart3,
    Building2,
    FileOutput,
    FilePlus2,
    LineChart,
    Search,
    Settings2,
    Users,
} from "lucide-react";

import { useNavigate } from "@tanstack/react-router";
import { useTranslation } from "react-i18next";

function QuickActions() {
    const navigate = useNavigate();
    const { t } = useTranslation();

    const actions = [
        {
            title: t(
                "dashboard.quickActions.startInvestigation.title",
            ),
            description: t(
                "dashboard.quickActions.startInvestigation.description",
            ),
            icon: FilePlus2,
            to: "/dashboard/new-investigation",
        },
        {
            title: t(
                "dashboard.quickActions.searchInvestigations.title",
            ),
            description: t(
                "dashboard.quickActions.searchInvestigations.description",
            ),
            icon: Search,
            to: "/dashboard/investigations",
        },
        {
            title: t(
                "dashboard.quickActions.viewReports.title",
            ),
            description: t(
                "dashboard.quickActions.viewReports.description",
            ),
            icon: BarChart3,
            to: "/dashboard/reports",
        },
        {
            title: t(
                "dashboard.quickActions.analytics.title",
            ),
            description: t(
                "dashboard.quickActions.analytics.description",
            ),
            icon: LineChart,
            to: "/dashboard/analytics",
        },
        {
            title: t(
                "dashboard.quickActions.organizations.title",
            ),
            description: t(
                "dashboard.quickActions.organizations.description",
            ),
            icon: Building2,
            to: "/dashboard/organizations",
        },
        {
            title: t(
                "dashboard.quickActions.exportCentre.title",
            ),
            description: t(
                "dashboard.quickActions.exportCentre.description",
            ),
            icon: FileOutput,
            to: "/dashboard/exports",
        },
        {
            title: t(
                "dashboard.quickActions.customerAdministration.title",
            ),
            description: t(
                "dashboard.quickActions.customerAdministration.description",
            ),
            icon: Settings2,
            to: "/dashboard/administration/customer",
        },
        {
            title: t(
                "dashboard.quickActions.userAdministration.title",
            ),
            description: t(
                "dashboard.quickActions.userAdministration.description",
            ),
            icon: Users,
            to: "/dashboard/administration/users",
        },
    ];

    return (
        <section className="mt-8">
            <div>
                <h2 className="text-xl font-semibold text-white">
                    {t("dashboard.quickActions.title")}
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    {t("dashboard.quickActions.subtitle")}
                </p>
            </div>

            <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {actions.map((action) => {
                    const Icon = action.icon;

                    return (
                        <button
                            key={action.to}
                            type="button"
                            onClick={() => {
                                void navigate({
                                    to: action.to,
                                });
                            }}
                            className="rounded-xl border border-slate-800 bg-slate-900 p-5 text-left transition hover:border-slate-600 hover:bg-slate-800"
                        >
                            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-800">
                                <Icon className="h-5 w-5 text-slate-200" />
                            </div>

                            <h3 className="mt-4 font-semibold text-white">
                                {action.title}
                            </h3>

                            <p className="mt-2 text-sm leading-6 text-slate-400">
                                {action.description}
                            </p>
                        </button>
                    );
                })}
            </div>
        </section>
    );
}

export default QuickActions;