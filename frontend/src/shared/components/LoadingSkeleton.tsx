interface LoadingSkeletonProps {
    className?: string;
}

function LoadingSkeleton({
    className = "",
}: LoadingSkeletonProps) {
    return (
        <div
            className={`animate-pulse rounded-lg bg-slate-800 ${className}`}
        />
    );
}

export default LoadingSkeleton;