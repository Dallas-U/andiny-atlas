import type { ReactNode } from "react";

type AppLayoutProps = {
    children: ReactNode;
};

function AppLayout({ children }: AppLayoutProps) {
    return (
        <div className="min-h-screen bg-slate-950 text-white">
            <header className="border-b border-slate-800 px-6 py-4">
                <h1 className="text-xl font-semibold">Andiny Atlas</h1>
            </header>

            <main className="p-6">{children}</main>
        </div>
    );
}

export default AppLayout;