import { Filter, Download, Calendar, Settings, ChevronDown, ChevronUp, Activity, AlertTriangle, CheckCircle, FileText, BarChart3, Zap } from "lucide-react";
import DatasetSelector from "./DatasetSelector";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Progress } from "@/components/ui/progress";
import { useState } from "react";

const DashboardSidebar = () => {
  const [filtersOpen, setFiltersOpen] = useState(true);
  const [quickStatsOpen, setQuickStatsOpen] = useState(true);
  const [actionsOpen, setActionsOpen] = useState(true);
  const [datasetOpen, setDatasetOpen] = useState(true);
  
  const [selectedMachine, setSelectedMachine] = useState("all");
  const [selectedRiskLevels, setSelectedRiskLevels] = useState<string[]>([]);
  const [selectedTimeRange, setSelectedTimeRange] = useState("24h");
  const [selectedDataset, setSelectedDataset] = useState("turbofan_data_medium.csv");

  const machines = [
    { id: "all", name: "All Machines", count: 12 },
    { id: "machine-001", name: "Machine-001", status: "error" },
    { id: "machine-002", name: "Machine-002", status: "warning" },
    { id: "machine-003", name: "Machine-003", status: "success" },
    { id: "machine-004", name: "Machine-004", status: "success" },
  ];

  const riskLevels = [
    { id: "low", name: "Low", count: 5, color: "success" },
    { id: "medium", name: "Medium", count: 4, color: "warning" },
    { id: "high", name: "High", count: 3, color: "error" },
  ];

  const quickStats = [
    { icon: Activity, label: "Active Machines", value: "12/15", color: "primary" },
    { icon: AlertTriangle, label: "Active Alerts", value: "7", color: "warning" },
    { icon: CheckCircle, label: "Healthy Systems", value: "8", color: "success" },
    { icon: Zap, label: "Efficiency", value: "94.2%", color: "primary" },
  ];

  const toggleRiskLevel = (riskId: string) => {
    setSelectedRiskLevels(prev => 
      prev.includes(riskId) 
        ? prev.filter(id => id !== riskId)
        : [...prev, riskId]
    );
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'error': return <div className="w-2 h-2 bg-error rounded-full animate-pulse" />;
      case 'warning': return <div className="w-2 h-2 bg-warning rounded-full" />;
      case 'success': return <div className="w-2 h-2 bg-success rounded-full" />;
      default: return null;
    }
  };

  return (
    <div className="space-y-4 sticky top-24">
      {/* Filters Section */}
      <Card className="glass-card">
        <Collapsible open={filtersOpen} onOpenChange={setFiltersOpen}>
          <CollapsibleTrigger asChild>
            <CardHeader className="pb-3 cursor-pointer hover:bg-primary/5 transition-colors rounded-t-lg">
              <CardTitle className="flex items-center justify-between text-base">
                <div className="flex items-center gap-2">
                  <Filter className="h-4 w-4 text-primary" />
                  Filters
                </div>
                {filtersOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </CardTitle>
            </CardHeader>
          </CollapsibleTrigger>
          
          <CollapsibleContent>
            <CardContent className="space-y-4 pt-0">
              {/* Machine Selection */}
              <div>
                <label className="text-sm font-medium text-muted-foreground mb-2 block">
                  Machine Selection
                </label>
                <div className="space-y-2">
                  {machines.map((machine) => (
                    <div
                      key={machine.id}
                      className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all hover:bg-primary/10 ${
                        selectedMachine === machine.id ? 'bg-primary/20 border border-primary/30' : 'border border-transparent'
                      }`}
                      onClick={() => setSelectedMachine(machine.id)}
                    >
                      <div className="flex items-center gap-2">
                        {machine.status && getStatusIcon(machine.status)}
                        <span className="text-sm">{machine.name}</span>
                      </div>
                      {machine.count && (
                        <Badge variant="outline" className="text-xs">
                          {machine.count}
                        </Badge>
                      )}
                    </div>
                  ))}
                </div>
              </div>

              <Separator />

              {/* Risk Level Filters */}
              <div>
                <label className="text-sm font-medium text-muted-foreground mb-2 block">
                  Risk Levels
                </label>
                <div className="space-y-2">
                  {riskLevels.map((risk) => (
                    <div
                      key={risk.id}
                      className={`flex items-center justify-between p-2 rounded-lg cursor-pointer transition-all hover:bg-${risk.color}/10 ${
                        selectedRiskLevels.includes(risk.id) ? `bg-${risk.color}/20 border border-${risk.color}/30` : 'border border-transparent'
                      }`}
                      onClick={() => toggleRiskLevel(risk.id)}
                    >
                      <div className="flex items-center gap-2">
                        <div className={`w-3 h-3 rounded-full bg-${risk.color}`} />
                        <span className="text-sm">{risk.name}</span>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {risk.count}
                      </Badge>
                    </div>
                  ))}
                </div>
              </div>

              <Separator />

              {/* Time Range */}
              <div>
                <label className="text-sm font-medium text-muted-foreground mb-2 flex items-center gap-2">
                  <Calendar className="h-4 w-4" />
                  Time Range
                </label>
                <select 
                  value={selectedTimeRange}
                  onChange={(e) => setSelectedTimeRange(e.target.value)}
                  className="w-full px-3 py-2 glass-card rounded-lg border border-border text-sm focus:ring-2 focus:ring-primary transition-all"
                >
                  <option value="1h">Last Hour</option>
                  <option value="24h">Last 24 Hours</option>
                  <option value="7d">Last 7 Days</option>
                  <option value="30d">Last 30 Days</option>
                  <option value="custom">Custom Range</option>
                </select>
              </div>
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* Quick Stats */}
      <Card className="glass-card">
        <Collapsible open={quickStatsOpen} onOpenChange={setQuickStatsOpen}>
          <CollapsibleTrigger asChild>
            <CardHeader className="pb-3 cursor-pointer hover:bg-primary/5 transition-colors rounded-t-lg">
              <CardTitle className="flex items-center justify-between text-base">
                <div className="flex items-center gap-2">
                  <BarChart3 className="h-4 w-4 text-primary" />
                  Quick Stats
                </div>
                {quickStatsOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </CardTitle>
            </CardHeader>
          </CollapsibleTrigger>
          
          <CollapsibleContent>
            <CardContent className="space-y-4 pt-0">
              {quickStats.map((stat, index) => (
                <div key={stat.label} className="flex items-center justify-between group hover:bg-primary/5 p-2 rounded-lg transition-colors">
                  <div className="flex items-center gap-3">
                    <stat.icon className={`h-4 w-4 text-${stat.color} group-hover:scale-110 transition-transform`} />
                    <span className="text-sm text-muted-foreground">{stat.label}</span>
                  </div>
                  <span className={`font-medium text-${stat.color}`}>{stat.value}</span>
                </div>
              ))}
              
              <div className="mt-4">
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-muted-foreground">System Health</span>
                  <span className="font-medium">87%</span>
                </div>
                <Progress value={87} className="h-2" />
              </div>
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* Actions */}
      <Card className="glass-card">
        <Collapsible open={actionsOpen} onOpenChange={setActionsOpen}>
          <CollapsibleTrigger asChild>
            <CardHeader className="pb-3 cursor-pointer hover:bg-primary/5 transition-colors rounded-t-lg">
              <CardTitle className="flex items-center justify-between text-base">
                <div className="flex items-center gap-2">
                  <Settings className="h-4 w-4 text-primary" />
                  Actions
                </div>
                {actionsOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </CardTitle>
            </CardHeader>
          </CollapsibleTrigger>
          
          <CollapsibleContent>
            <CardContent className="space-y-3 pt-0">
              <Button 
                variant="outline" 
                className="w-full justify-start gap-2 hover:bg-primary/10 hover:border-primary transition-all group"
              >
                <Download className="h-4 w-4 group-hover:scale-110 transition-transform" />
                Export CSV
              </Button>
              <Button 
                variant="outline" 
                className="w-full justify-start gap-2 hover:bg-primary/10 hover:border-primary transition-all group"
              >
                <FileText className="h-4 w-4 group-hover:scale-110 transition-transform" />
                Export PDF Report
              </Button>
              <Button 
                variant="outline" 
                className="w-full justify-start gap-2 hover:bg-primary/10 hover:border-primary transition-all group"
              >
                <Settings className="h-4 w-4 group-hover:scale-110 transition-transform" />
                Dashboard Settings
              </Button>
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* Dataset Selector */}
      <DatasetSelector
        selectedDataset={selectedDataset}
        onDatasetChange={setSelectedDataset}
        className="mt-4"
      />
    </div>
  );
};

export default DashboardSidebar;
