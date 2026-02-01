export type TaskStatus = 'todo' | 'in-progress' | 'complete';

export interface ApplicationStep {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  dueDate?: string;
  priority: 'low' | 'medium' | 'high';
}

export interface BonusTask {
  id: string;
  title: string;
  description: string;
  isComplete: boolean;
  category: 'extracurricular' | 'academic' | 'leadership' | 'community';
}

export interface UniversityProgram {
  id: string;
  universityName: string;
  programName: string;
  deadline: string;
  steps: ApplicationStep[];
  bonusTasks: BonusTask[];
  overallProgress: number;
}

export type RoadmapCategory = 'computer-science' | 'business' | 'health-sciences' | 'engineering' | 'arts' | 'risk-analysis';

export interface ApplicationRoadmap {
  id: string;
  name: string;
  category: RoadmapCategory;
  description: string;
  programIds: string[];
  icon: string;
}
