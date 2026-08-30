import {
    createContext,
    useCallback,
    useContext,
    useState,
    type ReactNode,
} from "react";
import {
    CheckCircle2,
    CircleAlert,
    Info,
    X,
} from "lucide-react";

type ToastType = "success" | "error" | "info";

interface Toast {
    id: number;
    message: string;
    type: ToastType;
}

interface ShowToastOptions {
    message: string;
    type?: ToastType;
    duration?: number;
}

interface ToastContextValue {
    showToast: (options: ShowToastOptions) => void;
}

interface ToastProviderProps {
    children: ReactNode;
}

const ToastContext = createContext<ToastContextValue | undefined>(
    undefined,
);

const toastStyles: Record<ToastType, string> = {
    success:
        "border-green-500/30 bg-green-950 text-green-200",
    error:
        "border-red-500/30 bg-red-950 text-red-200",
    info:
        "border-blue-500/30 bg-blue-950 text-blue-200",
};

const toastIcons = {
    success: CheckCircle2,
    error: CircleAlert,
    info: Info,
};

export function ToastProvider({
    children,
}: ToastProviderProps) {
    const [toasts, setToasts] = useState<Toast[]>([]);

    const removeToast = useCallback((id: number): void => {
        setToasts((currentToasts) =>
            currentToasts.filter((toast) => toast.id !== id),
        );
    }, []);

    const showToast = useCallback(
        ({
            message,
            type = "info",
            duration = 4000,
        }: ShowToastOptions): void => {
            const id = Date.now();

            setToasts((currentToasts) => [
                ...currentToasts,
                {
                    id,
                    message,
                    type,
                },
            ]);

            window.setTimeout(() => {
                removeToast(id);
            }, duration);
        },
        [removeToast],
    );

    return (
        <ToastContext.Provider value={{ showToast }}>
            {children}

            <div
                aria-live="polite"
                aria-atomic="true"
                className="fixed right-5 top-5 z-50 flex w-full max-w-sm flex-col gap-3"
            >
                {toasts.map((toast) => {
                    const Icon = toastIcons[toast.type];

                    return (
                        <div
                            key={toast.id}
                            role="status"
                            className={`flex items-start gap-3 rounded-xl border p-4 shadow-xl ${toastStyles[toast.type]}`}
                        >
                            <Icon className="mt-0.5 h-5 w-5 shrink-0" />

                            <p className="flex-1 text-sm font-medium leading-6">
                                {toast.message}
                            </p>

                            <button
                                type="button"
                                onClick={() => {
                                    removeToast(toast.id);
                                }}
                                aria-label="Dismiss notification"
                                className="rounded-md p-1 opacity-70 transition hover:bg-white/10 hover:opacity-100"
                            >
                                <X className="h-4 w-4" />
                            </button>
                        </div>
                    );
                })}
            </div>
        </ToastContext.Provider>
    );
}

export function useToast(): ToastContextValue {
    const context = useContext(ToastContext);

    if (!context) {
        throw new Error(
            "useToast must be used within a ToastProvider.",
        );
    }

    return context;
}