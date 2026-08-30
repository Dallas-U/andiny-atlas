import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";

import { useAuth } from "../../shared/auth/AuthContext";
import { saveToken } from "../../shared/auth/tokenStorage";
import { login } from "./auth.api";
import { loginSchema, type LoginFormData } from "./auth.schema";
import { useNavigate } from "@tanstack/react-router";

function LoginForm() {
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginFormData>({
        resolver: zodResolver(loginSchema),
        defaultValues: {
            email: "",
            password: "",
        },
    });

    const navigate = useNavigate();

    const { refreshAuthState } = useAuth();

    const onSubmit = async (data: LoginFormData) => {
        try {
            const token = await login(data);

            saveToken(token);
            refreshAuthState();

            await navigate({
                to: "/dashboard",
                replace: true,
            });
        } catch (error) {
            console.error("Login failed:", error);
        }
    };

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <div>
                <label
                    htmlFor="email"
                    className="mb-2 block text-sm font-medium text-slate-200"
                >
                    Email address
                </label>

                <input
                    id="email"
                    type="email"
                    autoComplete="email"
                    placeholder="name@example.com"
                    {...register("email")}
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-slate-500"
                />

                {errors.email && (
                    <p className="mt-2 text-sm text-red-400">
                        {errors.email.message}
                    </p>
                )}
            </div>

            <div>
                <label
                    htmlFor="password"
                    className="mb-2 block text-sm font-medium text-slate-200"
                >
                    Password
                </label>

                <input
                    id="password"
                    type="password"
                    autoComplete="current-password"
                    placeholder="Enter your password"
                    {...register("password")}
                    className="w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none placeholder:text-slate-600 focus:border-slate-500"
                />

                {errors.password && (
                    <p className="mt-2 text-sm text-red-400">
                        {errors.password.message}
                    </p>
                )}
            </div>

            <button
                type="submit"
                className="w-full rounded-lg bg-white px-4 py-3 font-semibold text-slate-950 transition hover:bg-slate-200"
            >
                Sign in
            </button>
        </form>
    );
}

export default LoginForm;