import { cn } from '@/lib/utils';
import { TaskStatus } from '@/types/application';

interface StatusBadgeProps {
  status: TaskStatus;
  className?: string;
}

const statusConfig: Record<TaskStatus, { label: string; className: string }> = {
  'todo': {
    label: 'TO DO',
    className: 'bg-muted text-muted-foreground border-2 border-border',
  },
  'in-progress': {
    label: 'IN PROGRESS',
    className: 'bg-[hsl(var(--status-in-progress))] text-[hsl(var(--status-in-progress-foreground))] border-2 border-border',
  },
  'complete': {
    label: 'DONE',
    className: 'bg-[hsl(var(--status-complete))] text-[hsl(var(--status-complete-foreground))] border-2 border-border',
  },
};

export function StatusBadge({ status, className }: StatusBadgeProps) {
  const config = statusConfig[status];

  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 text-xs font-mono font-bold uppercase tracking-wider',
        config.className,
        className
      )}
    >
      {config.label}
    </span>
  );
}
