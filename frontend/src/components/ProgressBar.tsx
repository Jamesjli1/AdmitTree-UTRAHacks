import { cn } from '@/lib/utils';

interface ProgressBarProps {
  value: number;
  className?: string;
  showLabel?: boolean;
}

export function ProgressBar({ value, className, showLabel = true }: ProgressBarProps) {
  return (
    <div className={cn('w-full', className)}>
      <div className="flex items-center justify-between mb-1">
        {showLabel && (
          <span className="text-sm font-mono font-bold">{value}%</span>
        )}
      </div>
      <div className="h-3 bg-muted border-2 border-border">
        <div
          className="h-full bg-[hsl(var(--status-complete))] transition-all duration-300"
          style={{ width: `${value}%` }}
        />
      </div>
    </div>
  );
}
