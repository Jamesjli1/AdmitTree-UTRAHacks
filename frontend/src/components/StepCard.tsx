import { ApplicationStep, TaskStatus } from '@/types/application';
import { StatusBadge } from './StatusBadge';
import { Calendar, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StepCardProps {
  step: ApplicationStep;
  index: number;
  onStatusToggle?: (e?: React.MouseEvent) => void;
}

const priorityConfig = {
  high: 'border-l-4 border-l-destructive',
  medium: 'border-l-4 border-l-[hsl(var(--status-in-progress))]',
  low: 'border-l-4 border-l-muted-foreground',
};

const getNextStatus = (currentStatus: TaskStatus): TaskStatus => {
  switch (currentStatus) {
    case 'todo':
      return 'in-progress';
    case 'in-progress':
      return 'complete';
    case 'complete':
      return 'todo';
    default:
      return 'todo';
  }
};

export function StepCard({ step, index, onStatusToggle }: StepCardProps) {
  const handleClick = (e: React.MouseEvent) => {
    if (onStatusToggle) {
      onStatusToggle(e);
    }
  };

  return (
    <div
      onClick={handleClick}
      className={cn(
        'bg-card border-2 border-border p-4 shadow-xs hover:shadow-sm transition-shadow',
        priorityConfig[step.priority],
        onStatusToggle && 'cursor-pointer hover:border-primary'
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 flex-1">
          <div className="flex items-center justify-center w-8 h-8 bg-primary text-primary-foreground font-mono font-bold text-sm border-2 border-border flex-shrink-0">
            {index + 1}
          </div>
          <div className="flex-1 min-w-0">
            <h4 className="font-bold text-sm mb-1">{step.title}</h4>
            <p className="text-xs text-muted-foreground mb-2">{step.description}</p>
            {step.dueDate && (
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
                <Calendar className="h-3 w-3" />
                <span className="font-mono">{step.dueDate}</span>
              </div>
            )}
          </div>
        </div>
        <div className="flex flex-col items-end gap-2">
          <StatusBadge status={step.status} />
          {step.priority === 'high' && step.status !== 'complete' && (
            <AlertCircle className="h-4 w-4 text-destructive" />
          )}
        </div>
      </div>
    </div>
  );
}
