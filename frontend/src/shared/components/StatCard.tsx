import type { ReactNode } from "react";

interface StatCardProps {
    title: string;
    value: number;
    icon: ReactNode;
    description?: string;
    className?: string;
}

function StatCard({
    title,
    value,
    icon,
    description,
    className = "",
}: StatCardProps) {
    return (
        <article
            className={`rounded-xl border border-slate-800 bg-slate-900 p-6 transition duration-200 hover:-translate-y-0.5 hover:border-slate-700 ${className}`}
        >
            <div className="flex items-start gap-4">
                <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-lg bg-slate-800">
                    {icon}
                </div>

                <div className="min-w-0">
                    <p className="text-sm font-medium text-slate-400">
                        {title}
                    </p>

                    <p className="mt-2 text-4xl font-bold tracking-tight text-white">
                        {value}
                    </p>
                </div>
            </div>

            {description && (
                <p className="mt-5 border-t border-slate-800 pt-4 text-sm text-slate-500">
                    {description}
                </p>
            )}
        </article>
    );
}

export default StatCard;