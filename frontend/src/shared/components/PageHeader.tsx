interface PageHeaderProps {
    title: string;
    description?: string;
    actions?: React.ReactNode;
}

function PageHeader({
    title,
    description,
    actions,
}: PageHeaderProps) {
    return (
        <div className="flex flex-col gap-4 border-b border-slate-800 pb-6 sm:flex-row sm:items-end sm:justify-between">
            <div>
                <h1 className="text-4xl font-bold tracking-tight text-white">
                    {title}
                </h1>

                {description && (
                    <p className="mt-3 max-w-2xl text-slate-400">
                        {description}
                    </p>
                )}
            </div>

            {actions && (
                <div className="flex items-center gap-3">
                    {actions}
                </div>
            )}
        </div>
    );
}

export default PageHeader;