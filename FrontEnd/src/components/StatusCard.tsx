import { LucideIcon } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface StatusCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  status?: "success" | "warning" | "error" | "info";
  description?: string;
  className?: string;
  trend?: "up" | "down" | "stable";
  percentage?: string;
}

const StatusCard = ({ 
  title, 
  value, 
  icon: Icon, 
  status = "info", 
  description, 
  className,
  trend,
  percentage 
}: StatusCardProps) => {
  const [isHovered, setIsHovered] = useState(false);

  const statusColors = {
    success: "text-success",
    warning: "text-warning",
    error: "text-error",
    info: "text-primary",
  };

  const statusGlows = {
    success: "hover:shadow-[0_0_30px_hsl(var(--success)/0.3)]",
    warning: "hover:shadow-[0_0_30px_hsl(var(--warning)/0.3)]",
    error: "hover:shadow-[0_0_30px_hsl(var(--error)/0.3)]",
    info: "hover:shadow-[0_0_30px_hsl(var(--primary)/0.3)]",
  };

  const statusBgs = {
    success: "from-success/10 to-success/5",
    warning: "from-warning/10 to-warning/5",
    error: "from-error/10 to-error/5",
    info: "from-primary/10 to-primary/5",
  };

  const trendColors = {
    up: "text-success",
    down: "text-error",
    stable: "text-muted-foreground",
  };

  return (
    <Card 
      className={cn(
        "glass-card card-3d group cursor-pointer relative overflow-hidden border-2 border-transparent hover:border-primary/30",
        statusGlows[status],
        className
      )}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {/* Animated background gradient */}
      <div className={cn(
        "absolute inset-0 bg-gradient-to-br opacity-0 group-hover:opacity-100 transition-all duration-500",
        statusBgs[status]
      )}></div>
      
      {/* Floating particles effect */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(3)].map((_, i) => (
          <div
            key={i}
            className={cn(
              "absolute w-1 h-1 rounded-full opacity-0 group-hover:opacity-60 transition-all duration-1000",
              statusColors[status].replace('text-', 'bg-')
            )}
            style={{
              left: `${20 + i * 30}%`,
              top: `${30 + i * 20}%`,
              animationDelay: `${i * 200}ms`,
              animation: isHovered ? 'float 2s ease-in-out infinite' : 'none'
            }}
          />
        ))}
      </div>
      
      <CardHeader className="relative pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm font-medium text-muted-foreground group-hover:text-foreground transition-colors duration-300">
            {title}
          </CardTitle>
          <div className="relative">
            <Icon className={cn(
              "h-6 w-6 transition-all duration-300 group-hover:scale-110 group-hover:rotate-12",
              statusColors[status]
            )} />
            <div className={cn(
              "absolute inset-0 rounded-full blur-sm opacity-0 group-hover:opacity-50 transition-all duration-300",
              statusColors[status].replace('text-', 'bg-')
            )}></div>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="relative pt-0">
        <div className="space-y-3">
          <div className="flex items-end gap-2">
            <div className={cn(
              "text-3xl font-bold transition-all duration-300 group-hover:scale-105",
              statusColors[status]
            )}>
              {value}
            </div>
            {percentage && trend && (
              <div className={cn(
                "text-sm font-medium transition-all duration-300",
                trendColors[trend]
              )}>
                {trend === 'up' ? '↗' : trend === 'down' ? '↘' : '→'} {percentage}
              </div>
            )}
          </div>
          
          {description && (
            <div className="overflow-hidden">
              <p className={cn(
                "text-xs text-muted-foreground transition-all duration-500 transform",
                isHovered ? "opacity-100 translate-y-0" : "opacity-0 translate-y-2"
              )}>
                {description}
              </p>
            </div>
          )}
        </div>
      </CardContent>

      {/* Shine effect on hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none"></div>
      
      {/* Pulse ring effect */}
      <div className={cn(
        "absolute inset-0 rounded-lg border-2 border-transparent group-hover:border-primary/50 transition-all duration-300 pointer-events-none",
        "group-hover:animate-pulse"
      )}></div>
    </Card>
  );
};

export default StatusCard;
