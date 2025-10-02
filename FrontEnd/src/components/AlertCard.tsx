import { AlertTriangle, AlertCircle, CheckCircle, Clock, X, Eye, Settings } from "lucide-react";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { useState } from "react";

interface AlertCardProps {
  level: "error" | "warning" | "success" | "info";
  title: string;
  message: string;
  timestamp?: string;
  machineId?: string;
  priority?: "low" | "medium" | "high" | "critical";
  onAcknowledge?: () => void;
  onDismiss?: () => void;
  onViewDetails?: () => void;
}

const AlertCard = ({ 
  level, 
  title, 
  message, 
  timestamp, 
  machineId,
  priority = "medium",
  onAcknowledge,
  onDismiss,
  onViewDetails
}: AlertCardProps) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isAcknowledged, setIsAcknowledged] = useState(false);

  const icons = {
    error: AlertCircle,
    warning: AlertTriangle,
    success: CheckCircle,
    info: AlertCircle,
  };

  const styles = {
    error: "border-error/50 bg-error/5 hover:bg-error/10",
    warning: "border-warning/50 bg-warning/5 hover:bg-warning/10",
    success: "border-success/50 bg-success/5 hover:bg-success/10",
    info: "border-primary/50 bg-primary/5 hover:bg-primary/10",
  };

  const iconColors = {
    error: "text-error",
    warning: "text-warning",
    success: "text-success",
    info: "text-primary",
  };

  const priorityColors = {
    low: "bg-muted text-muted-foreground",
    medium: "bg-warning/20 text-warning",
    high: "bg-error/20 text-error",
    critical: "bg-error text-error-foreground animate-pulse",
  };

  const animations = {
    error: "animate-glow",
    warning: "animate-pulse-slow",
    success: "",
    info: "",
  };

  const Icon = icons[level];

  const handleAcknowledge = () => {
    setIsAcknowledged(true);
    onAcknowledge?.();
  };

  const handleDismiss = () => {
    onDismiss?.();
  };

  return (
    <Alert className={cn(
      "glass-card card-3d group cursor-pointer relative overflow-hidden transition-all duration-300",
      styles[level],
      animations[level],
      isAcknowledged && "opacity-60 scale-95"
    )}>
      {/* Priority indicator */}
      <div className={cn(
        "absolute top-0 left-0 w-1 h-full",
        level === 'error' ? 'bg-error' : 
        level === 'warning' ? 'bg-warning' : 
        level === 'success' ? 'bg-success' : 'bg-primary'
      )} />

      {/* Header */}
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-3">
          <div className="relative">
            <Icon className={cn("h-5 w-5 transition-transform group-hover:scale-110", iconColors[level])} />
            {level === 'error' && (
              <div className="absolute inset-0 rounded-full bg-error/20 animate-ping" />
            )}
          </div>
          <div className="flex items-center gap-2">
            <AlertTitle className="font-semibold text-foreground">{title}</AlertTitle>
            {machineId && (
              <Badge variant="outline" className="text-xs">
                {machineId}
              </Badge>
            )}
            <Badge className={cn("text-xs", priorityColors[priority])}>
              {priority.toUpperCase()}
            </Badge>
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          {onViewDetails && (
            <Button
              variant="ghost"
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                onViewDetails();
              }}
              className="h-8 w-8 p-0 hover:bg-primary/20"
            >
              <Eye className="h-4 w-4" />
            </Button>
          )}
          {onDismiss && (
            <Button
              variant="ghost"
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                handleDismiss();
              }}
              className="h-8 w-8 p-0 hover:bg-error/20"
            >
              <X className="h-4 w-4" />
            </Button>
          )}
        </div>
      </div>

      {/* Content */}
      <AlertDescription 
        className="text-sm text-muted-foreground cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className={cn(
          "transition-all duration-300",
          isExpanded ? "max-h-none" : "max-h-12 overflow-hidden"
        )}>
          {message}
        </div>
        
        {message.length > 100 && (
          <button className="text-primary hover:underline text-xs mt-1">
            {isExpanded ? 'Show less' : 'Show more'}
          </button>
        )}
      </AlertDescription>

      {/* Footer */}
      <div className="flex items-center justify-between mt-4 pt-3 border-t border-border/50">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <Clock className="h-3 w-3" />
          {timestamp || 'Just now'}
        </div>

        <div className="flex items-center gap-2">
          {onAcknowledge && !isAcknowledged && (
            <Button
              variant="outline"
              size="sm"
              onClick={(e) => {
                e.stopPropagation();
                handleAcknowledge();
              }}
              className="h-7 px-3 text-xs hover:bg-primary/20 hover:border-primary/50"
            >
              Acknowledge
            </Button>
          )}
          {isAcknowledged && (
            <Badge variant="outline" className="text-xs">
              ✓ Acknowledged
            </Badge>
          )}
        </div>
      </div>

      {/* Hover shine effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000 pointer-events-none" />
    </Alert>
  );
};

export default AlertCard;
