import type { ReactNode } from "react";

type AuthLayoutProps = {
    children: ReactNode;
};

function AuthLayout({ children }: AuthLayoutProps) {
    return (
        <div className="flex min-h-screen items-center justify-center bg-slate-950 px-6 text-white">
            <div className="w-full max-w-md">
                <header className="mb-8 text-center">
                    <h1 className="text-3xl font-semibold">Andiny Atlas</h1>
                    <p className="mt-2 text-sm text-slate-400">
                        Investigation Platform
                    </p>
                </header>

                <main>{children}</main>
            </div>
        </div>
    );
}

export default AuthLayout;