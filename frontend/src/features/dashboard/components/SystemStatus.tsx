import { CheckCircle2 } from "lucide-react";

import Card from "../../../shared/components/Card";
import { useAuth } from "../../../shared/auth/AuthContext";

function SystemStatus() {
    const { user } = useAuth();

    const statusItems = [
        {
            label: "Authentication",
            value: "Authenticated",
        },
        {
            label: "Current role",
            value: user?.role ?? "Unknown",
        },
        {
            label: "Environment",
            value: import.meta.env.DEV
                ? "Development"
                : "Production",
        },
    ];

    return (
        <section className="mt-10 mb-12">
            <div>
                <h2 className="text-xl font-semibold text-white">
                    System Status
                </h2>

                <p className="mt-1 text-sm text-slate-400">
                    Current operational information for your Atlas session.
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