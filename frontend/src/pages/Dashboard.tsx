import { useState, useEffect } from 'react';
import { globalBonusTasks, applicationRoadmaps } from '@/data/mockData';
import { DashboardHeader } from '@/components/DashboardHeader';
import { ProgramCard } from '@/components/ProgramCard';
import { BonusTaskCard } from '@/components/BonusTaskCard';
import { RoadmapSidebar } from '@/components/RoadmapSidebar';
import { ChatbotButton } from '@/components/ChatbotButton';
import { FocusedProgramView } from '@/components/FocusedProgramView';
import { TaskTimeline } from '@/components/TaskTimeline';
import { Star, Trash2 } from 'lucide-react';
import { UniversityProgram, TaskStatus } from '@/types/application';
import { useToast } from '@/hooks/use-toast';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import { Button } from '@/components/ui/button';

const Dashboard = () => {
  const [focusedProgramId, setFocusedProgramId] = useState<string | null>(null);
  const [activeRoadmapId, setActiveRoadmapId] = useState<string | null>(null);
  const [programs, setPrograms] = useState<UniversityProgram[]>([]);
  const { toast } = useToast();

  // Load programs from localStorage on mount
  useEffect(() => {
    const storedPrograms = localStorage.getItem("currentPrograms");
    if (storedPrograms) {
      try {
        const parsedPrograms = JSON.parse(storedPrograms);
        setPrograms(parsedPrograms);
      } catch (error) {
        console.error("Failed to parse stored programs:", error);
      }
    }
  }, []);

  // Calculate stats
  const totalPrograms = programs.length;
  const allSteps = programs.flatMap(p => p.steps);
  const completedSteps = allSteps.filter(s => s.status === 'complete').length;
  const inProgressSteps = allSteps.filter(s => s.status === 'in-progress').length;
  const todoSteps = allSteps.filter(s => s.status === 'todo').length;
  const totalSteps = allSteps.length;
  const overallProgress = totalSteps > 0 ? Math.round((completedSteps / totalSteps) * 100) : 0;

  const completedBonusTasks = globalBonusTasks.filter(t => t.isComplete).length;

  // Update program progress when steps change
  const updateProgramProgress = (program: UniversityProgram): UniversityProgram => {
    const completed = program.steps.filter(s => s.status === 'complete').length;
    const total = program.steps.length;
    const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
    return { ...program, overallProgress: progress };
  };

  // Handle step status change
  const handleStepStatusChange = (programId: string, stepId: string, newStatus: TaskStatus) => {
    setPrograms(prevPrograms => {
      const updatedPrograms = prevPrograms.map(program => {
        if (program.id === programId) {
          const updatedSteps = program.steps.map(step =>
            step.id === stepId ? { ...step, status: newStatus } : step
          );
          const updatedProgram = { ...program, steps: updatedSteps };
          return updateProgramProgress(updatedProgram);
        }
        return program;
      });

      // Persist to localStorage
      localStorage.setItem("currentPrograms", JSON.stringify(updatedPrograms));
      
      // Also update the current roadmap if it exists
      const currentRoadmap = localStorage.getItem("currentRoadmap");
      if (currentRoadmap) {
        try {
          const roadmap = JSON.parse(currentRoadmap);
          roadmap.programs = updatedPrograms;
          localStorage.setItem("currentRoadmap", JSON.stringify(roadmap));
        } catch (error) {
          console.error("Failed to update roadmap:", error);
        }
      }

      return updatedPrograms;
    });
  };

  // Get focused program
  const focusedProgram = focusedProgramId
    ? programs.find(p => p.id === focusedProgramId)
    : null;

  // Filter programs by active roadmap
  const activeRoadmap = activeRoadmapId
    ? applicationRoadmaps.find(r => r.id === activeRoadmapId)
    : null;

  const displayedPrograms = activeRoadmap
    ? programs.filter(p => activeRoadmap.programIds.includes(p.id))
    : programs;

  const handleSelectRoadmap = (id: string) => {
    setActiveRoadmapId(id === activeRoadmapId ? null : id);
    setFocusedProgramId(null);
  };

  const handleCreateRoadmap = () => {
    // TODO: Implement roadmap creation modal
    console.log('Create new roadmap');
  };

  const handleProgramClick = (programId: string) => {
    setFocusedProgramId(programId);
  };

  const handleTimelineTaskClick = (stepId: string, programId: string) => {
    setFocusedProgramId(programId);
  };

  const handleClearData = () => {
    localStorage.removeItem("currentPrograms");
    localStorage.removeItem("currentRoadmap");
    localStorage.removeItem("userRoadmaps");
    setPrograms([]);
    setFocusedProgramId(null);
    setActiveRoadmapId(null);
    toast({
      title: "Data Cleared",
      description: "All stored programs have been removed from your dashboard.",
    });
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container max-w-6xl py-8 px-4">
        <div className="flex items-center gap-4 mb-6">
          <RoadmapSidebar
            roadmaps={applicationRoadmaps}
            activeRoadmapId={activeRoadmapId}
            onSelectRoadmap={handleSelectRoadmap}
            onCreateRoadmap={handleCreateRoadmap}
          />
          {activeRoadmap && (
            <span className="text-sm text-muted-foreground font-mono">
              Viewing: {activeRoadmap.name}
            </span>
          )}
        </div>

        {/* Timeline at the top */}
        {!focusedProgram && (
          <TaskTimeline
            programs={displayedPrograms}
            onTaskClick={handleTimelineTaskClick}
          />
        )}

        {focusedProgram ? (
          <FocusedProgramView
            program={focusedProgram}
            onBack={() => setFocusedProgramId(null)}
            onStepStatusChange={handleStepStatusChange}
          />
        ) : (
          <>
            <DashboardHeader
              totalPrograms={displayedPrograms.length}
              overallProgress={overallProgress}
              completedTasks={completedSteps}
              inProgressTasks={inProgressSteps}
              todoTasks={todoSteps}
              totalTasks={totalSteps}
            />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Main Content - Program Cards */}
              <div className="lg:col-span-2 space-y-4">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-bold uppercase tracking-wider">
                    {activeRoadmap ? activeRoadmap.name : 'My Programs'}
                  </h2>
                  <div className="flex items-center gap-3">
                    <span className="text-sm text-muted-foreground font-mono">
                      {displayedPrograms.length} active
                    </span>
                    {programs.length > 0 && (
                      <AlertDialog>
                        <AlertDialogTrigger asChild>
                          <Button variant="outline" size="sm" className="gap-2">
                            <Trash2 className="h-4 w-4" />
                            Clear Data
                          </Button>
                        </AlertDialogTrigger>
                        <AlertDialogContent>
                          <AlertDialogHeader>
                            <AlertDialogTitle>Clear All Programs?</AlertDialogTitle>
                            <AlertDialogDescription>
                              This will remove all programs from your dashboard. This action cannot be undone.
                              You can always create a new roadmap by completing the intake form again.
                            </AlertDialogDescription>
                          </AlertDialogHeader>
                          <AlertDialogFooter>
                            <AlertDialogCancel>Cancel</AlertDialogCancel>
                            <AlertDialogAction onClick={handleClearData} className="bg-destructive text-destructive-foreground hover:bg-destructive/90">
                              Clear All Data
                            </AlertDialogAction>
                          </AlertDialogFooter>
                        </AlertDialogContent>
                      </AlertDialog>
                    )}
                  </div>
                </div>
                {displayedPrograms.length > 0 ? (
                  displayedPrograms.map(program => (
                    <div
                      key={program.id}
                      onClick={() => handleProgramClick(program.id)}
                      className="cursor-pointer"
                    >
                      <ProgramCard 
                        program={program} 
                        onStepStatusChange={handleStepStatusChange}
                      />
                    </div>
                  ))
                ) : (
                  <div className="bg-card border-2 border-border p-8 text-center">
                    <p className="text-muted-foreground">
                      {programs.length === 0 
                        ? "No programs found. Please complete the intake form to get recommendations." 
                        : "No programs in this roadmap yet."}
                    </p>
                  </div>
                )}
              </div>

              {/* Sidebar - Bonus Tasks */}
              <div className="lg:col-span-1">
                <div className="sticky top-8">
                  <div className="bg-card border-2 border-border shadow-sm">
                    <div className="p-4 border-b-2 border-border bg-[hsl(var(--status-bonus))]">
                      <div className="flex items-center gap-2 text-[hsl(var(--status-bonus-foreground))]">
                        <Star className="h-5 w-5" />
                        <h2 className="font-bold uppercase tracking-wider">Bonus Tasks</h2>
                      </div>
                      <p className="text-[hsl(var(--status-bonus-foreground))] text-xs mt-1 opacity-90">
                        Strengthen your application profile
                      </p>
                    </div>
                    <div className="p-4">
                      <div className="flex items-center justify-between mb-4">
                        <span className="text-sm text-muted-foreground">Completed</span>
                        <span className="font-mono font-bold">{completedBonusTasks}/{globalBonusTasks.length}</span>
                      </div>
                      <div className="space-y-3">
                        {globalBonusTasks.map(task => (
                          <BonusTaskCard key={task.id} task={task} />
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </div>

      {/* Chatbot Button */}
      <ChatbotButton />
    </div>
  );
};

export default Dashboard;
