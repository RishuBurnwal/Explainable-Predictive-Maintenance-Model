import { ArrowRight, Activity, Shield, Brain, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";

const Hero = () => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    setIsVisible(true);
  }, []);

  const scrollToDashboard = () => {
    const element = document.getElementById('dashboard');
    element?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section id="home" className="relative min-h-[80vh] flex items-center justify-center gradient-hero overflow-hidden">
      {/* Animated Background Pattern */}
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAxOGMzLjMxNCAwIDYgMi42ODYgNiA2cy0yLjY4NiA2LTYgNi02LTIuNjg2LTYtNiAyLjY4Ni02IDYtNnptLTEyIDEyYzMuMzE0IDAgNiAyLjY4NiA2IDZzLTIuNjg2IDYtNiA2LTYtMi42ODYtNi02IDIuNjg2LTYgNi02eiIgc3Ryb2tlPSJoc2woMTg5IDk0JSA0MyUgLyAwLjA1KSIvPjwvZz48L3N2Zz4=')] opacity-20 animate-pulse-slow"></div>
      
      {/* Floating Icons */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <Activity className="absolute top-20 left-10 h-8 w-8 text-primary/30 animate-bounce" style={{ animationDelay: '0s' }} />
        <Shield className="absolute top-32 right-20 h-6 w-6 text-primary/20 animate-bounce" style={{ animationDelay: '1s' }} />
        <Brain className="absolute bottom-40 left-20 h-10 w-10 text-primary/25 animate-bounce" style={{ animationDelay: '2s' }} />
        <TrendingUp className="absolute bottom-20 right-10 h-7 w-7 text-primary/30 animate-bounce" style={{ animationDelay: '0.5s' }} />
      </div>
      
      <div className="container mx-auto px-4 text-center relative z-10">
        <div className={`max-w-5xl mx-auto space-y-8 transition-all duration-1000 ${
          isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
        }`}>
          {/* Main Title */}
          <div className="space-y-4">
            <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold leading-tight break-words">
              <span className="bg-gradient-to-r from-foreground via-primary to-foreground bg-clip-text text-transparent animate-gradient">
                Explainable Predictive
              </span>
              <br />
              <span className="bg-gradient-to-r from-primary via-foreground to-primary bg-clip-text text-transparent animate-gradient">
                Maintenance System
              </span>
            </h1>
            
            <div className="h-1 w-32 bg-gradient-to-r from-primary to-transparent mx-auto rounded-full"></div>
          </div>

          {/* Subtitle */}
          <p className="text-base sm:text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto leading-relaxed break-words px-4">
            Live monitoring, anomaly detection, and explainable AI insights for proactive machine health management
          </p>

          {/* Feature Pills */}
          <div className="flex flex-wrap justify-center gap-4 py-4">
            {[
              { icon: Activity, text: "Real-time Monitoring" },
              { icon: Brain, text: "AI Predictions" },
              { icon: Shield, text: "Anomaly Detection" },
              { icon: TrendingUp, text: "Trend Analysis" }
            ].map((feature, index) => (
              <div 
                key={feature.text}
                className={`flex items-center gap-2 px-4 py-2 glass-card rounded-full text-sm transition-all duration-500 hover:scale-105 hover:glow-effect ${
                  isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
                }`}
                style={{ transitionDelay: `${index * 100}ms` }}
              >
                <feature.icon className="h-4 w-4 text-primary" />
                <span>{feature.text}</span>
              </div>
            ))}
          </div>

          {/* CTA Button */}
          <div className={`pt-4 transition-all duration-700 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`} style={{ transitionDelay: '400ms' }}>
            <Button 
              size="lg"
              onClick={scrollToDashboard}
              className="group gradient-primary text-lg px-10 py-6 hover:opacity-90 transition-all duration-500 hover:scale-110 card-3d glow-effect shadow-2xl hover:shadow-primary/30 relative overflow-hidden"
            >
              <span className="relative z-10 flex items-center">
                Start Monitoring
                <ArrowRight className="ml-3 h-6 w-6 group-hover:translate-x-2 transition-transform duration-300" />
              </span>
              
              {/* Button shine effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-700"></div>
            </Button>
          </div>

          {/* Stats */}
          <div className={`grid grid-cols-2 md:grid-cols-4 gap-8 pt-12 transition-all duration-1000 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`} style={{ transitionDelay: '600ms' }}>
            {[
              { value: "99.9%", label: "Uptime" },
              { value: "24/7", label: "Monitoring" },
              { value: "< 1ms", label: "Response Time" },
              { value: "100+", label: "Machines Tracked" }
            ].map((stat, index) => (
              <div key={stat.label} className="text-center group">
                <div className="text-2xl md:text-3xl font-bold text-primary group-hover:scale-110 transition-transform duration-300">
                  {stat.value}
                </div>
                <div className="text-sm text-muted-foreground mt-1">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
