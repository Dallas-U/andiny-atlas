import { ArrowLeft } from "lucide-react";
import { useNavigate } from "@tanstack/react-router";

interface BackButtonProps {
    to?: string;
    label?: string;
}

function BackButton({
    to = "/dashboard",
    label = "Back to dashboard",
}: BackButtonProps) {
    const navigate = useNavigate();

    function handleBack(): void {
        void navigate({
            to,
        });
    }

    return (
        <button
            type="button"
            onClick={handleBack}
            className="inline-flex items-center gap-2 text-sm font-medium text-slate-400 transition hover:text-white"
        >
            <ArrowLeft className="h-4 w-4" />

            {label}
        </button>
    );
}

export default BackButton;