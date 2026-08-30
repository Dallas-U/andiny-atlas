import type { ReactNode } from "react";

interface EmptyStateProps {
    title: string;
    description: string;
    icon?: ReactNode;
}

function EmptyState({
    title,
    description,
    icon,
}: EmptyStateProps) {
    return (
        <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-700 bg-slate-900 px-8 py-14 text-center">
            {icon && (
                <div className="mb-4 text-slate-500">
                    {icon}
                </div>
            )}

            <h3 className="text-lg font-semibold text-white">
                {title}
            </h3>

            <p className="mt-2 max-w-md text-sm leading-6 text-slate-400">
                {description}
            </p>
        </div>
    );
}

export default EmptyState;