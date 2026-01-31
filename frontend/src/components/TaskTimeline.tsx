import { useMemo } from 'react';
import { format, parseISO, isToday, isPast, isFuture, differenceInDays } from 'date-fns';
import { ApplicationStep, UniversityProgram } from '@/types/application';
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area';
import { cn } from '@/lib/utils';
import { Calendar, Clock, CheckCircle2, AlertCircle } from 'lucide-react';

interface TimelineTask {
  step: ApplicationStep;
  programName: string;
  universityName: string;
  date: Date;
}

interface TaskTimelineProps {
  programs: UniversityProgram[];
  onTaskClick?: (stepId: string, programId: string) => void;
}

export const TaskTimeline = ({ programs, onTaskClick }: TaskTimelineProps) => {
  // Extract all tasks with dates and sort by date
  const timelineTasks = useMemo(() => {
    const tasks: TimelineTask[] = [];
    
    programs.forEach(program => {
      program.steps.forEach(step => {
        if (step.dueDate) {
          tasks.push({
            step,
            programName: program.programName,
            universityName: program.universityName,
            date: parseISO(step.dueDate),
          });
        }
      });
    });
    
    return tasks.sort((a, b) => a.date.getTime() - b.date.getTime());
  }, [programs]);

  const getStatusStyles = (status: string, date: Date) => {
    if (status === 'complete') {
      return 'bg-[hsl(var(--status-complete))] border-[hsl(var(--status-complete))] text-[hsl(var(--status-complete-foreground))]';
    }
    if (isPast(date) && status !== 'complete') {
      return 'bg-destructive border-destructive text-destructive-foreground';
    }
    if (status === 'in-progress') {
      return 'bg-[hsl(var(--status-in-progress))] border-[hsl(var(--status-in-progress))] text-[hsl(var(--status-in-progress-foreground))]';
    }
    return 'bg-card border-border text-foreground';
  };

  const getDaysLabel = (date: Date) => {
    const days = differenceInDays(date, new Date());
    if (isToday(date)) return 'Today';
    if (days === 1) return 'Tomorrow';
    if (days === -1) return 'Yesterday';
    if (days < 0) return `${Math.abs(days)}d overdue`;
    return `${days}d left`;
  };

  if (timelineTasks.length === 0) {
    return null;
  }

  return (
    <div className="mb-6">
      <div className="flex items-center gap-2 mb-3">
        <Calendar className="h-4 w-4 text-muted-foreground" />
        <h3 className="text-sm font-bold uppercase tracking-wider text-muted-foreground">Timeline</h3>
      </div>
      
      <div className="bg-card border-2 border-border p-4">
        <ScrollArea className="w-full">
          <div className="flex gap-4 pb-3 min-w-max">
            {timelineTasks.map((task, index) => {
              const isOverdue = isPast(task.date) && task.step.status !== 'complete';
              const isComplete = task.step.status === 'complete';
              
              return (
                <div
                  key={`${task.step.id}-${index}`}
                  className={cn(
                    "relative flex-shrink-0 w-48 p-3 border-2 transition-all cursor-pointer hover:translate-y-[-2px] hover:shadow-md",
                    getStatusStyles(task.step.status, task.date)
                  )}
                  onClick={() => {
                    const program = programs.find(p => 
                      p.steps.some(s => s.id === task.step.id)
                    );
                    if (program && onTaskClick) {
                      onTaskClick(task.step.id, program.id);
                    }
                  }}
                >
                  {/* Date Header */}
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-mono font-bold">
                      {format(task.date, 'MMM d')}
                    </span>
                    <span className={cn(
                      "text-xs font-mono",
                      isOverdue && "text-destructive-foreground font-bold",
                      isComplete && "text-[hsl(var(--status-complete-foreground))]"
                    )}>
                      {getDaysLabel(task.date)}
                    </span>
                  </div>
                  
                  {/* Task Title */}
                  <p className="text-sm font-semibold line-clamp-2 mb-1">
                    {task.step.title}
                  </p>
                  
                  {/* Program/University */}
                  <p className="text-xs opacity-80 line-clamp-1">
                    {task.universityName} - {task.programName}
                  </p>
                  
                  {/* Status Icon */}
                  <div className="absolute top-2 right-2">
                    {isComplete ? (
                      <CheckCircle2 className="h-4 w-4" />
                    ) : isOverdue ? (
                      <AlertCircle className="h-4 w-4" />
                    ) : (
                      <Clock className="h-4 w-4 opacity-60" />
                    )}
                  </div>
                  
                  {/* Timeline connector */}
                  {index < timelineTasks.length - 1 && (
                    <div className="absolute right-[-1rem] top-1/2 w-4 h-0.5 bg-border" />
                  )}
                </div>
              );
            })}
          </div>
          <ScrollBar orientation="horizontal" />
        </ScrollArea>
      </div>
    </div>
  );
};
