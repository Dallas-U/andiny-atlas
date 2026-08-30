import type { ReactNode } from "react";

interface CardProps {
    children: ReactNode;
    className?: string;
}

function Card({
    children,
    className = "",
}: CardProps) {
    return (
        <section
            className={`rounded-xl border border-slate-800 bg-slate-900 p-6 shadow-sm ${className}`}
        >
            {children}
        </section>
    );
}

export default Card;