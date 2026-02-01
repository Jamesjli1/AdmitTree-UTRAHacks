import { useState } from "react";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { GraduationCap, TrendingUp } from "lucide-react";
import { cn } from "@/lib/utils";

interface ProgramRanking {
    university: string;
    program: string;
    score: number;
    breakdown: {
        academic: number;
        interest: number;
        ec: number;
        coop_fit: number;
    };
}

interface ProgramSelectionModalProps {
    open: boolean;
    rankings: ProgramRanking[];
    onConfirm: (selectedIndices: number[]) => void;
    onCancel: () => void;
}

export function ProgramSelectionModal({
    open,
    rankings,
    onConfirm,
    onCancel,
}: ProgramSelectionModalProps) {
    const [selectedIndices, setSelectedIndices] = useState<Set<number>>(new Set());

    // Get top 6 programs (or all if less than 6)
    const topPrograms = rankings.slice(0, Math.min(6, rankings.length));

    const toggleSelection = (index: number) => {
        const newSelected = new Set(selectedIndices);
        if (newSelected.has(index)) {
            newSelected.delete(index);
        } else {
            newSelected.add(index);
        }
        setSelectedIndices(newSelected);
    };

    const handleConfirm = () => {
        onConfirm(Array.from(selectedIndices));
        setSelectedIndices(new Set());
    };

    const handleCancel = () => {
        setSelectedIndices(new Set());
        onCancel();
    };

    return (
        <Dialog open={open} onOpenChange={(isOpen) => !isOpen && handleCancel()}>
            <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
                <DialogHeader>
                    <DialogTitle>Select Programs for Your Dashboard</DialogTitle>
                    <DialogDescription>
                        Choose the programs you'd like to track. We've selected the top 6 matches for you based on your profile.
                    </DialogDescription>
                </DialogHeader>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 py-4">
                    {topPrograms.map((program, index) => {
                        const isSelected = selectedIndices.has(index);
                        return (
                            <Card
                                key={index}
                                className={cn(
                                    "cursor-pointer transition-all hover:shadow-md border-2",
                                    isSelected
                                        ? "border-primary bg-primary/5"
                                        : "border-border hover:border-primary/50"
                                )}
                                onClick={() => toggleSelection(index)}
                            >
                                <CardContent className="p-4">
                                    <div className="flex items-start justify-between gap-3">
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center gap-2 mb-2">
                                                <GraduationCap className="h-4 w-4 flex-shrink-0 text-primary" />
                                                <h3 className="font-bold text-sm truncate">
                                                    {program.university}
                                                </h3>
                                            </div>
                                            <p className="text-sm font-medium text-muted-foreground mb-3">
                                                {program.program}
                                            </p>

                                            {/* Score Badge */}
                                            <div className="flex items-center gap-2">
                                                <div className="flex items-center gap-1 px-2 py-1 bg-primary/10 text-primary rounded-md">
                                                    <TrendingUp className="h-3 w-3" />
                                                    <span className="text-xs font-bold font-mono">
                                                        {program.score.toFixed(1)}%
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex-shrink-0" onClick={(e) => e.stopPropagation()}>
                                            <Checkbox
                                                checked={isSelected}
                                                onCheckedChange={() => toggleSelection(index)}
                                            />
                                        </div>
                                    </div>
                                </CardContent>
                            </Card>
                        );
                    })}
                </div>

                {topPrograms.length === 0 && (
                    <div className="text-center py-8 text-muted-foreground">
                        <p>No programs found. Please try adjusting your profile.</p>
                    </div>
                )}

                <DialogFooter>
                    <Button variant="outline" onClick={handleCancel}>
                        Cancel
                    </Button>
                    <Button
                        onClick={handleConfirm}
                        disabled={selectedIndices.size === 0}
                    >
                        Add {selectedIndices.size > 0 ? `${selectedIndices.size} ` : ""}
                        Program{selectedIndices.size !== 1 ? "s" : ""} to Dashboard
                    </Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    );
}

