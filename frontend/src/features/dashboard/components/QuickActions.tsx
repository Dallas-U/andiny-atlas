import {
    BarChart3,
    Building2,
    FileOutput,
    FilePlus2,
    LineChart,
    Search,
} from "lucide-react";
import { useNavigate } from "@tanstack/react-router";

const actions = [
    {
        title: "Start investigation",
        description: "Open a new customer support investigation.",
        icon: FilePlus2,
        to: "/dashboard/new-investigation",
    },
    {
        title: "Search investigations",
        description: "Find and review existing investigation records.",
        icon: Search,
        to: "/dashboard/investigations",
    },
    {
        title: "View reports",
        description: "Access investigation and operational reports.",
        icon: BarChart3,
        to: "/dashboard/reports",
    },
    {
        title: "Analytics",
        description: "View operational investigation analytics.",
        icon: LineChart,
        to: "/dashboard/analytics",
    },
    {
        title: "Organizations",
        description:
            "View organization analytics and enterprise performance metrics.",
        icon: Building2,
        to: "/dashboard/organizations",
    },
    {
        title: "Export Centre",
        description:
            "Export reports, analytics and investigation records.",
        icon: FileOutput,
        to: "/dashboard/exports",
    },
];

function QuickActions() {
    const navigate = useNavigate();

    return (
        <section className="mt-8">
            <div>
                <h2 className="text-xl font-semibold text-white">
                    Quick Actions
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Choose a task to continue working in Andiny Atlas.
                </p>
            </div>

            <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
                {actions.map((action) => {
                    const Icon = action.icon;

                    return (
                        <button
                            key={action.title}
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