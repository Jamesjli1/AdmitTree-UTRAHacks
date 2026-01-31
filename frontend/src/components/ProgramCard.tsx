import { useState } from 'react';
import { UniversityProgram, TaskStatus } from '@/types/application';
import { ProgressBar } from './ProgressBar';
import { StepCard } from './StepCard';
import { ChevronDown, ChevronUp, Calendar, GraduationCap } from 'lucide-react';
import { cn } from '@/lib/utils';

interface ProgramCardProps {
  program: UniversityProgram;
  onStepStatusChange?: (programId: string, stepId: string, newStatus: TaskStatus) => void;
}

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

export function ProgramCard({ program, onStepStatusChange }: ProgramCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const completedSteps = program.steps.filter(s => s.status === 'complete').length;
  const inProgressSteps = program.steps.filter(s => s.status === 'in-progress').length;
  const todoSteps = program.steps.filter(s => s.status === 'todo').length;

  const handleStepClick = (stepId: string, e: React.MouseEvent) => {
    e.stopPropagation(); // Prevent card expansion when clicking step
    if (!onStepStatusChange) return;
    const step = program.steps.find(s => s.id === stepId);
    if (step) {
      const newStatus = getNextStatus(step.status);
      onStepStatusChange(program.id, stepId, newStatus);
    }
  };

  return (
    <div className="bg-card border-2 border-border shadow-sm hover:shadow-md transition-shadow">
      {/* Card Header - Always Visible */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full p-5 text-left hover:bg-accent/50 transition-colors"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <GraduationCap className="h-5 w-5 flex-shrink-0" />
              <h3 className="font-bold text-lg truncate">{program.universityName}</h3>
            </div>
            <p className="text-muted-foreground font-medium mb-3">{program.programName}</p>
            
            <div className="flex items-center gap-4 text-sm mb-4">
              <div className="flex items-center gap-1.5 text-muted-foreground">
                <Calendar className="h-4 w-4" />
                <span className="font-mono">{program.deadline}</span>
              </div>
            </div>

            <ProgressBar value={program.overallProgress} />
          </div>
          
          <div className="flex flex-col items-end gap-2">
            {isExpanded ? (
              <ChevronUp className="h-6 w-6" />
            ) : (
              <ChevronDown className="h-6 w-6" />
            )}
          </div>
        </div>

        {/* Status Summary Pills */}
        <div className="flex flex-wrap gap-2 mt-4">
          <span className="inline-flex items-center gap-1.5 px-2 py-1 bg-[hsl(var(--status-complete))] text-[hsl(var(--status-complete-foreground))] text-xs font-mono font-bold border-2 border-border">
            {completedSteps} Done
          </span>
          <span className="inline-flex items-center gap-1.5 px-2 py-1 bg-[hsl(var(--status-in-progress))] text-[hsl(var(--status-in-progress-foreground))] text-xs font-mono font-bold border-2 border-border">
            {inProgressSteps} In Progress
          </span>
          <span className="inline-flex items-center gap-1.5 px-2 py-1 bg-muted text-muted-foreground text-xs font-mono font-bold border-2 border-border">
            {todoSteps} To Do
          </span>
        </div>
      </button>

      {/* Expanded Content - Steps */}
      <div
        className={cn(
          'overflow-hidden transition-all duration-300',
          isExpanded ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'
        )}
      >
        <div className="border-t-2 border-border p-5">
          <h4 className="font-bold text-sm uppercase tracking-wider mb-4">Application Steps</h4>
          <div className="space-y-3">
            {program.steps.map((step, index) => (
              <StepCard 
                key={step.id} 
                step={step} 
                index={index}
                onStatusToggle={(e) => handleStepClick(step.id, e)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
