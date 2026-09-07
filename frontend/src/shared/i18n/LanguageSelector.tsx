import type { ChangeEvent } from "react";
import { Languages } from "lucide-react";
import { useTranslation } from "react-i18next";

const languages = [
    {
        code: "en",
        label: "English",
    },
    {
        code: "fr",
        label: "Français",
    },
    {
        code: "es",
        label: "Español",
    },
] as const;

function LanguageSelector() {
    const { i18n } = useTranslation();

    function handleLanguageChange(
        event: ChangeEvent<HTMLSelectElement>,
    ) {
        void i18n.changeLanguage(
            event.target.value,
        );
    }

    return (
        <div className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-slate-700 bg-slate-900">
                <Languages className="h-4 w-4 text-slate-300" />
            </div>

            <select
                value={i18n.language}
                onChange={handleLanguageChange}
                aria-label="Select language"
                className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-white outline-none transition hover:border-slate-500 focus:border-slate-400"
            >
                {languages.map((language) => (
                    <option
                        key={language.code}
                        value={language.code}
                    >
                        {language.label}
                    </option>
                ))}
            </select>
        </div>
    );
}

export default LanguageSelector;