import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { GraduationCap, Target, Calendar, CheckCircle, ArrowRight } from "lucide-react";
import { useNavigate } from "react-router-dom";

const LandingPage = () => {
    const navigate = useNavigate();

    const features = [
        {
            icon: Target,
            title: "Personalized Roadmaps",
            description: "Get a custom application roadmap tailored to your university and program choices",
        },
        {
            icon: Calendar,
            title: "Deadline Tracking",
            description: "Never miss an important deadline with our timeline and notification system",
        },
        {
            icon: CheckCircle,
            title: "Step-by-Step Guidance",
            description: "Follow clear steps from application to acceptance with progress tracking",
        },
    ];

    return (
        <div className="min-h-screen bg-background">
            {/* Hero Section */}
            <section className="relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-background to-secondary/5" />
                <div className="relative container mx-auto px-4 py-20 lg:py-32">
                    <div className="max-w-3xl mx-auto text-center">
                        <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full mb-6">
                            <GraduationCap className="h-5 w-5" />
                            <span className="text-sm font-medium">University Application Tracker</span>
                        </div>

                        <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6 leading-tight">
                            Navigate Your Path to{" "}
                            <span className="text-primary">University Success</span>
                        </h1>

                        <p className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
                            Create a personalized roadmap for your university applications. Track deadlines,
                            manage tasks, and stay organized throughout your application journey.
                        </p>

                        <div className="flex flex-col sm:flex-row gap-4 justify-center">
                            <Button
                                size="lg"
                                className="gap-2"
                                onClick={() => navigate("/intake")}
                            >
                                Create Your Roadmap
                                <ArrowRight className="h-5 w-5" />
                            </Button>
                            <Button
                                variant="outline"
                                size="lg"
                                onClick={() => navigate("/dashboard")}
                            >
                                View Demo Dashboard
                            </Button>
                        </div>
                    </div>
                </div>
            </section>

            {/* Features Section */}
            <section className="py-20 bg-muted/30">
                <div className="container mx-auto px-4">
                    <div className="text-center mb-12">
                        <h2 className="text-3xl md:text-4xl font-bold text-foreground mb-4">
                            Everything You Need to Stay on Track
                        </h2>
                        <p className="text-muted-foreground max-w-2xl mx-auto">
                            Our application tracker helps you manage every aspect of your university applications
                        </p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
                        {features.map((feature, index) => (
                            <Card key={index} className="bg-card border-border hover:shadow-lg transition-shadow">
                                <CardContent className="p-6 text-center">
                                    <div className="inline-flex items-center justify-center w-12 h-12 bg-primary/10 text-primary rounded-lg mb-4">
                                        <feature.icon className="h-6 w-6" />
                                    </div>
                                    <h3 className="text-xl font-semibold text-foreground mb-2">
                                        {feature.title}
                                    </h3>
                                    <p className="text-muted-foreground">
                                        {feature.description}
                                    </p>
                                </CardContent>
                            </Card>
                        ))}
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="py-20">
                <div className="container mx-auto px-4">
                    <Card className="bg-primary text-primary-foreground max-w-4xl mx-auto">
                        <CardContent className="p-8 md:p-12 text-center">
                            <h2 className="text-2xl md:text-3xl font-bold mb-4">
                                Ready to Start Your Application Journey?
                            </h2>
                            <p className="text-primary-foreground/80 mb-6 max-w-xl mx-auto">
                                Answer a few questions about your goals and we'll generate a personalized
                                roadmap to guide you through every step.
                            </p>
                            <Button
                                variant="secondary"
                                size="lg"
                                className="gap-2"
                                onClick={() => navigate("/intake")}
                            >
                                Get Started Now
                                <ArrowRight className="h-5 w-5" />
                            </Button>
                        </CardContent>
                    </Card>
                </div>
            </section>

            {/* Footer */}
            <footer className="border-t border-border py-8">
                <div className="container mx-auto px-4 text-center text-muted-foreground">
                    <p>© 2025 University Application Tracker. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
