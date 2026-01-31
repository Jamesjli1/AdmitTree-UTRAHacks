import { ApplicationRoadmap, RoadmapCategory } from '@/types/application';
import { Sheet, SheetContent, SheetHeader, SheetTitle, SheetTrigger } from '@/components/ui/sheet';
import { Button } from '@/components/ui/button';
import { Map, Plus, Code, Briefcase, HeartPulse, Wrench, Palette, TrendingUp } from 'lucide-react';
import { cn } from '@/lib/utils';

interface RoadmapSidebarProps {
  roadmaps: ApplicationRoadmap[];
  activeRoadmapId: string | null;
  onSelectRoadmap: (id: string) => void;
  onCreateRoadmap: () => void;
}

const categoryIcons: Record<RoadmapCategory, React.ComponentType<{ className?: string }>> = {
  'computer-science': Code,
  'business': Briefcase,
  'health-sciences': HeartPulse,
  'engineering': Wrench,
  'arts': Palette,
  'risk-analysis': TrendingUp,
};

const categoryColors: Record<RoadmapCategory, string> = {
  'computer-science': 'bg-blue-100 text-blue-700 border-blue-300',
  'business': 'bg-emerald-100 text-emerald-700 border-emerald-300',
  'health-sciences': 'bg-rose-100 text-rose-700 border-rose-300',
  'engineering': 'bg-amber-100 text-amber-700 border-amber-300',
  'arts': 'bg-purple-100 text-purple-700 border-purple-300',
  'risk-analysis': 'bg-cyan-100 text-cyan-700 border-cyan-300',
};

export function RoadmapSidebar({ 
  roadmaps, 
  activeRoadmapId, 
  onSelectRoadmap, 
  onCreateRoadmap 
}: RoadmapSidebarProps) {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button 
          variant="outline" 
          size="sm" 
          className="gap-2 border-2 border-border font-bold uppercase tracking-wider text-xs"
        >
          <Map className="h-4 w-4" />
          Roadmaps
        </Button>
      </SheetTrigger>
      <SheetContent side="left" className="w-80 border-r-2 border-border">
        <SheetHeader className="border-b-2 border-border pb-4">
          <SheetTitle className="flex items-center gap-2 font-bold uppercase tracking-wider">
            <Map className="h-5 w-5" />
            Application Roadmaps
          </SheetTitle>
        </SheetHeader>
        
        <div className="mt-6 space-y-3">
          {roadmaps.map((roadmap) => {
            const Icon = categoryIcons[roadmap.category];
            const isActive = roadmap.id === activeRoadmapId;
            
            return (
              <button
                key={roadmap.id}
                onClick={() => onSelectRoadmap(roadmap.id)}
                className={cn(
                  'w-full p-4 text-left border-2 transition-all',
                  isActive 
                    ? 'border-primary bg-primary/5 shadow-md' 
                    : 'border-border hover:border-primary/50 hover:bg-accent/50'
                )}
              >
                <div className="flex items-start gap-3">
                  <div className={cn(
                    'p-2 border-2',
                    categoryColors[roadmap.category]
                  )}>
                    <Icon className="h-4 w-4" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-bold text-sm truncate">{roadmap.name}</h4>
                    <p className="text-xs text-muted-foreground mt-1 line-clamp-2">
                      {roadmap.description}
                    </p>
                    <span className="text-xs font-mono text-muted-foreground mt-2 block">
                      {roadmap.programIds.length} programs
                    </span>
                  </div>
                </div>
              </button>
            );
          })}
        </div>

        <div className="absolute bottom-6 left-6 right-6">
          <Button 
            onClick={onCreateRoadmap}
            className="w-full gap-2 border-2 border-border font-bold uppercase tracking-wider"
          >
            <Plus className="h-4 w-4" />
            New Roadmap
          </Button>
        </div>
      </SheetContent>
    </Sheet>
  );
}
