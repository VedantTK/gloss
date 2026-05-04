import React from "react";

interface SkeletonProps {
  className?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ className = "" }) => (
  <div
    className={`relative overflow-hidden bg-obsidian-700 rounded ${className}`}
    style={{
      background: "linear-gradient(90deg, #18181f 25%, #26263a 50%, #18181f 75%)",
      backgroundSize: "200% 100%",
      animation: "shimmer 1.5s infinite",
    }}
  />
);

export const StockCardSkeleton: React.FC = () => (
  <div className="bg-obsidian-800 border border-white/5 rounded-xl p-4 space-y-3">
    <div className="flex justify-between items-start">
      <Skeleton className="h-5 w-20" />
      <Skeleton className="h-5 w-14 rounded-full" />
    </div>
    <Skeleton className="h-7 w-28" />
    <div className="flex gap-2">
      <Skeleton className="h-3 w-full" />
    </div>
    <div className="flex justify-between">
      <Skeleton className="h-4 w-16" />
      <Skeleton className="h-4 w-16" />
    </div>
  </div>
);

export const PanelSkeleton: React.FC = () => (
  <div className="space-y-3">
    {Array.from({ length: 5 }).map((_, i) => (
      <StockCardSkeleton key={i} />
    ))}
  </div>
);
