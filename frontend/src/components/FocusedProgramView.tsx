import { UniversityProgram, TaskStatus } from '@/types/application';
import { ProgressBar } from './ProgressBar';
import { StepCard } from './StepCard';
import { Button } from '@/components/ui/button';
import { ArrowLeft, Calendar, GraduationCap, Clock } from 'lucide-react';

interface FocusedProgramViewProps {
  program: UniversityProgram;
  onBack: () => void;
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

export function FocusedProgramView({ program, onBack, onStepStatusChange }: FocusedProgramViewProps) {
  const completedSteps = program.steps.filter(s => s.status === 'complete').length;
  const inProgressSteps = program.steps.filter(s => s.status === 'in-progress').length;
  const todoSteps = program.steps.filter(s => s.status === 'todo').length;

  const handleStepClick = (stepId: string) => {
    if (!onStepStatusChange) return;
    const step = program.steps.find(s => s.id === stepId);
    if (step) {
      const newStatus = getNextStatus(step.status);
      onStepStatusChange(program.id, stepId, newStatus);
    }
  };

  // Calculate days until deadline
  const deadline = new Date(program.deadline);
  const today = new Date();
  const daysUntilDeadline = Math.ceil((deadline.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));

  return (
    <div className="space-y-6">
      {/* Back Button */}
      <Button
        variant="ghost"
        onClick={onBack}
        className="gap-2 font-bold uppercase tracking-wider text-sm hover:bg-accent"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to All Programs
      </Button>

      {/* Program Header */}
      <div className="bg-card border-2 border-border p-6">
        <div className="flex items-start justify-between gap-6">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2">
              <GraduationCap className="h-8 w-8" />
              <div>
                <h1 className="text-2xl font-bold">{program.universityName}</h1>
                <p className="text-lg text-muted-foreground font-medium">{program.programName}</p>
              </div>
            </div>

            <div className="flex items-center gap-6 mt-6">
              <div className="flex items-center gap-2 text-muted-foreground">
                <Calendar className="h-5 w-5" />
                <span className="font-mono font-bold">{program.deadline}</span>
              </div>
              <div className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                <span className={`font-mono font-bold ${daysUntilDeadline < 30 ? 'text-destructive' : 'text-muted-foreground'}`}>
                  {daysUntilDeadline > 0 ? `${daysUntilDeadline} days left` : 'Deadline passed'}
                </span>
              </div>
            </div>
          </div>

          <div className="text-right">
            <div className="text-4xl font-mono font-bold">{program.overallProgress}%</div>
            <p className="text-sm text-muted-foreground uppercase tracking-wider">Complete</p>
          </div>
        </div>

        <div className="mt-6">
          <ProgressBar value={program.overallProgress} />
        </div>

        {/* Status Summary */}
        <div className="flex flex-wrap gap-3 mt-6">
          <div className="flex items-center gap-2 px-4 py-2 bg-[hsl(var(--status-complete))] text-[hsl(var(--status-complete-foreground))] border-2 border-border">
            <span className="text-2xl font-mono font-bold">{completedSteps}</span>
            <span className="text-sm uppercase tracking-wider">Done</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-[hsl(var(--status-in-progress))] text-[hsl(var(--status-in-progress-foreground))] border-2 border-border">
            <span className="text-2xl font-mono font-bold">{inProgressSteps}</span>
            <span className="text-sm uppercase tracking-wider">In Progress</span>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-muted text-muted-foreground border-2 border-border">
            <span className="text-2xl font-mono font-bold">{todoSteps}</span>
            <span className="text-sm uppercase tracking-wider">To Do</span>
          </div>
        </div>
      </div>

      {/* Application Steps */}
      <div className="bg-card border-2 border-border">
        <div className="p-4 border-b-2 border-border bg-muted">
          <h2 className="font-bold uppercase tracking-wider">Application Steps</h2>
        </div>
        <div className="p-6 space-y-4">
          {program.steps.map((step, index) => (
            <StepCard 
              key={step.id} 
              step={step} 
              index={index} 
              onStatusToggle={() => handleStepClick(step.id)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
