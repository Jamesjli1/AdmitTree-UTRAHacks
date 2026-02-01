import { BonusTask } from '@/types/application';
import { Check, Star, Users, BookOpen, Award, Heart } from 'lucide-react';
import { cn } from '@/lib/utils';

interface BonusTaskCardProps {
  task: BonusTask;
}

const categoryConfig = {
  extracurricular: { icon: Star, label: 'Extracurricular' },
  academic: { icon: BookOpen, label: 'Academic' },
  leadership: { icon: Award, label: 'Leadership' },
  community: { icon: Heart, label: 'Community' },
};

export function BonusTaskCard({ task }: BonusTaskCardProps) {
  const { icon: Icon, label } = categoryConfig[task.category];

  return (
    <div
      className={cn(
        'bg-card border-2 border-border p-4 shadow-xs transition-all',
        task.isComplete && 'bg-accent/30'
      )}
    >
      <div className="flex items-start gap-3">
        <div
          className={cn(
            'flex items-center justify-center w-8 h-8 border-2 border-border flex-shrink-0 transition-colors',
            task.isComplete
              ? 'bg-[hsl(var(--status-bonus))] text-[hsl(var(--status-bonus-foreground))]'
              : 'bg-muted text-muted-foreground'
          )}
        >
          {task.isComplete ? (
            <Check className="h-4 w-4" />
          ) : (
            <Star className="h-4 w-4" />
          )}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-1">
            <h4 className={cn('font-bold text-sm', task.isComplete && 'line-through text-muted-foreground')}>
              {task.title}
            </h4>
          </div>
          <p className="text-xs text-muted-foreground mb-2">{task.description}</p>
          <div className="flex items-center gap-1.5">
            <Icon className="h-3 w-3 text-[hsl(var(--status-bonus))]" />
            <span className="text-xs font-mono font-bold text-[hsl(var(--status-bonus))] uppercase">
              {label}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
