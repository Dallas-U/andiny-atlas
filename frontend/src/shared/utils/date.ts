export function formatRelativeDate(value: string): string {
    const date = new Date(value);
    const now = new Date();
    const differenceInSeconds = Math.round(
        (date.getTime() - now.getTime()) / 1000,
    );

    const formatter = new Intl.RelativeTimeFormat("en", {
        numeric: "auto",
    });

    const ranges = [
        { unit: "year", seconds: 60 * 60 * 24 * 365 },
        { unit: "month", seconds: 60 * 60 * 24 * 30 },
        { unit: "week", seconds: 60 * 60 * 24 * 7 },
        { unit: "day", seconds: 60 * 60 * 24 },
        { unit: "hour", seconds: 60 * 60 },
        { unit: "minute", seconds: 60 },
        { unit: "second", seconds: 1 },
    ] as const;

    for (const range of ranges) {
        if (
            Math.abs(differenceInSeconds) >= range.seconds ||
            range.unit === "second"
        ) {
            return formatter.format(
                Math.round(differenceInSeconds / range.seconds),
                range.unit,
            );
        }
    }

    return "just now";
}

export function formatExactDate(value: string): string {
    return new Date(value).toLocaleString();
}