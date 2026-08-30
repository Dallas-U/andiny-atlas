import LoginForm from "../features/auth/LoginForm";

function LoginPage() {
    return (
        <section className="rounded-xl border border-slate-800 bg-slate-900 p-8 shadow-xl">
            <div className="mb-6">
                <h2 className="text-2xl font-semibold text-white">
                    Sign in
                </h2>

                <p className="mt-2 text-sm text-slate-400">
                    Enter your credentials to access Andiny Atlas.
                </p>
            </div>

            <LoginForm />
        </section>
    );
}

export default LoginPage;