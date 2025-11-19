import { Filter, Download, Calendar, Settings, ChevronDown, ChevronUp, Activity, AlertTriangle, CheckCircle, FileText, BarChart3, Zap, Brain, Cpu, TrendingUp } from "lucide-react";
import DatasetSelector from "./DatasetSelector";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import { Progress } from "@/components/ui/progress";
import { useState } from "react";

const DashboardSidebar = ({ sensorData }: { sensorData?: any }) => {
  const [filtersOpen, setFiltersOpen] = useState(true);
  const [quickStatsOpen, setQuickStatsOpen] = useState(true);
  const [actionsOpen, setActionsOpen] = useState(true);
  const [datasetOpen, setDatasetOpen] = useState(true);
  const [aiModelsOpen, setAiModelsOpen] = useState(true);
  const [featureAnalysisOpen, setFeatureAnalysisOpen] = useState(true);
  
  const [selectedMachine, setSelectedMachine] = useState("all");
  const [selectedRiskLevels, setSelectedRiskLevels] = useState<string[]>([]);
  const [selectedTimeRange, setSelectedTimeRange] = useState("24h");
  const [selectedDataset, setSelectedDataset] = useState("turbofan_data_medium.csv");

  const machines = [
    { id: "all", name: "All Production Lines", count: 16 },
    { id: "production-line-a", name: "Production Line A", status: "warning", count: 6 },
    { id: "production-line-b", name: "Production Line B", status: "success", count: 3 },
    { id: "production-line-c", name: "Production Line C", status: "success", count: 3 },
    { id: "quality-control", name: "Quality Control", status: "success", count: 2 },
    { id: "cooling-system", name: "Central Cooling", status: "error", count: 2 },
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

  // AI Models with dynamic status
  const getAiModels = () => {
    // Default models info
    const defaultModels = [
      { name: "XGBoost", type: "RUL Prediction", accuracy: "89.5%", status: "active", color: "success" },
      { name: "LightGBM", type: "Failure Risk", accuracy: "91.2%", status: "active", color: "success" },
      { name: "Isolation Forest", type: "Anomaly Detection", accuracy: "93.8%", status: "active", color: "success" },
    ];
    
    // If we have real model info from sensorData, use it
    if (sensorData?.model_info) {
      return Object.entries(sensorData.model_info).map(([key, modelInfo]: [string, any]) => ({
        name: modelInfo.type || key,
        type: modelInfo.purpose || "AI Model",
        accuracy: modelInfo.accuracy || "90%",
        status: modelInfo.status === 'ready' ? "active" : modelInfo.status || "active",
        color: modelInfo.status === 'ready' ? "success" : modelInfo.status === 'error' ? "error" : "warning"
      }));
    }
    
    return defaultModels;
  };

  // AI Predictions by Category (dynamic based on sensor data)
  const getAiCategoryPredictions = () => {
    if (!sensorData?.sensor_stats) {
      return [
        { category: "Production Line A", sensors: 6, prediction: "Normal", confidence: 94.2, risk: "Low", trend: "stable" },
        { category: "Production Line B", sensors: 3, prediction: "Warning", confidence: 78.5, risk: "Medium", trend: "up" },
        { category: "Production Line C", sensors: 3, prediction: "Normal", confidence: 96.8, risk: "Low", trend: "stable" },
        { category: "Quality Control", sensors: 2, prediction: "Normal", confidence: 98.1, risk: "Low", trend: "stable" },
        { category: "Central Cooling", sensors: 2, prediction: "Critical", confidence: 42.3, risk: "High", trend: "down" },
      ];
    }
    
    // Extract real data from sensor stats
    const stats = sensorData.sensor_stats;
    return [
      { 
        category: "Production Line A", 
        sensors: 6, 
        prediction: stats.critical_sensors > 2 ? "Critical" : stats.warning_sensors > 1 ? "Warning" : "Normal", 
        confidence: stats.health_score || 94.2, 
        risk: stats.critical_sensors > 2 ? "High" : stats.warning_sensors > 1 ? "Medium" : "Low", 
        trend: stats.critical_sensors > 1 ? "down" : "stable" 
      },
      { 
        category: "Production Line B", 
        sensors: 3, 
        prediction: stats.critical_sensors > 1 ? "Warning" : "Normal", 
        confidence: Math.max(70, stats.health_score || 78.5), 
        risk: stats.critical_sensors > 1 ? "Medium" : "Low", 
        trend: "stable" 
      },
      { 
        category: "Production Line C", 
        sensors: 3, 
        prediction: "Normal", 
        confidence: 96.8, 
        risk: "Low", 
        trend: "stable" 
      },
      { 
        category: "Quality Control", 
        sensors: 2, 
        prediction: "Normal", 
        confidence: 98.1, 
        risk: "Low", 
        trend: "stable" 
      },
      { 
        category: "Central Cooling", 
        sensors: 2, 
        prediction: stats.critical_sensors > 0 ? "Critical" : "Normal", 
        confidence: stats.critical_sensors > 0 ? 42.3 : 95.0, 
        risk: stats.critical_sensors > 0 ? "High" : "Low", 
        trend: stats.critical_sensors > 0 ? "down" : "stable" 
      },
    ];
  };

  // Individual Sensor Predictions (dynamic based on sensor data)
  const getSensorPredictions = () => {
    if (!sensorData?.predictions) {
      return [
        { name: "Core Temperature Sensor", location: "Production Line A", prediction: "Normal", confidence: 95.2, risk: "Low" },
        { name: "Fan Vibration Monitor", location: "Production Line A", prediction: "Warning", confidence: 82.7, risk: "Medium" },
        { name: "Hydraulic Pump Temperature", location: "Production Line B", prediction: "Normal", confidence: 97.1, risk: "Low" },
        { name: "Bearing Vibration Sensor", location: "Production Line A", prediction: "Critical", confidence: 38.5, risk: "High" },
        { name: "Cooling System Temp", location: "Central Cooling", prediction: "Critical", confidence: 41.8, risk: "High" },
      ];
    }
    
    // Extract real data from predictions
    const rulValue = sensorData.predictions.rul?.value || 0;
    const riskClass = sensorData.predictions.risk?.risk_class || "Low";
    const isAnomaly = sensorData.predictions.anomaly?.is_anomaly || false;
    
    // Generate dynamic predictions based on actual AI results
    return [
      { 
        name: "RUL Prediction", 
        location: "System Wide", 
        prediction: rulValue < 50 ? "Critical" : rulValue < 100 ? "Warning" : "Normal", 
        confidence: Math.min(99, Math.max(30, rulValue > 0 ? (rulValue / 300) * 100 : 85)), 
        risk: rulValue < 50 ? "High" : rulValue < 100 ? "Medium" : "Low" 
      },
      { 
        name: "Risk Assessment", 
        location: "Failure Probability", 
        prediction: riskClass.includes("High") ? "Critical" : riskClass.includes("Medium") ? "Warning" : "Normal", 
        confidence: Math.min(95, Math.max(40, (sensorData.predictions.risk?.risk_score || 0.7) * 100)), 
        risk: riskClass.includes("High") ? "High" : riskClass.includes("Medium") ? "Medium" : "Low" 
      },
      { 
        name: "Anomaly Detection", 
        location: "Pattern Analysis", 
        prediction: isAnomaly ? "Critical" : "Normal", 
        confidence: isAnomaly ? 45 : 92, 
        risk: isAnomaly ? "High" : "Low" 
      },
      { 
        name: "Sensor Health", 
        location: "Network Status", 
        prediction: sensorData.sensor_stats?.critical_sensors > 2 ? "Critical" : sensorData.sensor_stats?.warning_sensors > 3 ? "Warning" : "Normal", 
        confidence: sensorData.sensor_stats?.health_score || 88, 
        risk: sensorData.sensor_stats?.critical_sensors > 2 ? "High" : sensorData.sensor_stats?.warning_sensors > 3 ? "Medium" : "Low" 
      },
      { 
        name: "Maintenance Forecast", 
        location: "Schedule Planning", 
        prediction: rulValue < 30 ? "Critical" : rulValue < 72 ? "Warning" : "Normal", 
        confidence: Math.min(98, Math.max(50, rulValue > 0 ? (rulValue / 200) * 100 : 75)), 
        risk: rulValue < 30 ? "High" : rulValue < 72 ? "Medium" : "Low" 
      },
    ];
  };

  const topFeatures = [
    { name: "Temperature", importance: 0.85, trend: "up" },
    { name: "Vibration", importance: 0.72, trend: "stable" },
    { name: "Pressure", importance: 0.58, trend: "down" },
    { name: "RPM", importance: 0.45, trend: "up" },
    { name: "Load", importance: 0.32, trend: "stable" },
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
              {/* Production Group Selection */}
              <div>
                <label className="text-sm font-medium text-muted-foreground mb-2 block">
                  Production Group
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

      {/* AI Models Section */}
      <Card className="glass-card">
        <Collapsible open={aiModelsOpen} onOpenChange={setAiModelsOpen}>
          <CollapsibleTrigger asChild>
            <CardHeader className="pb-3 cursor-pointer hover:bg-primary/5 transition-colors rounded-t-lg">
              <CardTitle className="flex items-center justify-between text-base">
                <div className="flex items-center gap-2">
                  <Brain className="h-4 w-4 text-primary" />
                  AI Models
                </div>
                {aiModelsOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </CardTitle>
            </CardHeader>
          </CollapsibleTrigger>
          
          <CollapsibleContent>
            <CardContent className="space-y-3 pt-0">
              {getAiModels().map((model) => (
                <div key={model.name} className="space-y-2 p-3 glass-card rounded-lg hover:bg-primary/5 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Cpu className="h-4 w-4 text-primary" />
                      <span className="text-sm font-medium">{model.name}</span>
                    </div>
                    <Badge variant="outline" className="text-xs">
                      <div className={`w-2 h-2 rounded-full bg-${model.color} mr-1`} />
                      {model.status === 'error' ? 'Error' : 'Active'}
                    </Badge>
                  </div>
                  <div className="text-xs text-muted-foreground">{model.type}</div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">Accuracy</span>
                    <span className={`font-semibold ${model.color === 'error' ? 'text-error' : model.color === 'warning' ? 'text-warning' : 'text-success'}`}>{model.accuracy}</span>
                  </div>
                </div>
              ))}
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* AI Predictions by Category */}
      <Card className="glass-card">
        <Collapsible open={featureAnalysisOpen} onOpenChange={setFeatureAnalysisOpen}>
          <CollapsibleTrigger asChild>
            <CardHeader className="pb-3 cursor-pointer hover:bg-primary/5 transition-colors rounded-t-lg">
              <CardTitle className="flex items-center justify-between text-base">
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-primary" />
                  AI Predictions by Category
                </div>
                {featureAnalysisOpen ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </CardTitle>
            </CardHeader>
          </CollapsibleTrigger>
          
          <CollapsibleContent>
            <CardContent className="space-y-3 pt-0">
              <p className="text-xs text-muted-foreground mb-3">Predictive maintenance status by production line</p>
              {getAiCategoryPredictions().map((category, index) => (
                <div key={category.category} className="space-y-2 p-3 glass-card rounded-lg hover:bg-primary/5 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium">{category.category}</span>
                      <Badge variant="outline" className="text-xs">
                        {category.sensors} sensors
                      </Badge>
                    </div>
                    <div className="flex items-center gap-1">
                      {category.trend === 'up' && <TrendingUp className="w-3 h-3 text-error" />}
                      {category.trend === 'down' && <TrendingUp className="w-3 h-3 text-success rotate-180" />}
                      {category.trend === 'stable' && <div className="w-3 h-0.5 bg-muted-foreground" />}
                      <span className={`text-xs font-semibold ${category.risk === 'High' ? 'text-error' : category.risk === 'Medium' ? 'text-warning' : 'text-success'}`}>
                        {category.prediction}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">Confidence</span>
                    <span className="font-semibold">{category.confidence.toFixed(1)}%</span>
                  </div>
                  <Progress 
                    value={category.confidence} 
                    className={`h-1.5 ${category.risk === 'High' ? 'bg-error/20' : category.risk === 'Medium' ? 'bg-warning/20' : 'bg-success/20'}`} 
                  />
                </div>
              ))}
              <div className="mt-4 p-2 bg-primary/10 rounded-lg">
                <p className="text-xs text-muted-foreground">
                  <strong>AI Insight:</strong> Central Cooling system requires immediate attention
                </p>
              </div>
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* Individual Sensor Predictions */}
      <Card className="glass-card">
        <Collapsible open={true} onOpenChange={() => {}}>
          <CollapsibleTrigger asChild>
            <CardHeader className="pb-3 cursor-pointer hover:bg-primary/5 transition-colors rounded-t-lg">
              <CardTitle className="flex items-center justify-between text-base">
                <div className="flex items-center gap-2">
                  <Cpu className="h-4 w-4 text-primary" />
                  Individual Sensor Predictions
                </div>
                <ChevronDown className="h-4 w-4" />
              </CardTitle>
            </CardHeader>
          </CollapsibleTrigger>
          
          <CollapsibleContent>
            <CardContent className="space-y-3 pt-0">
              <p className="text-xs text-muted-foreground mb-3">AI predictions for critical sensors</p>
              {getSensorPredictions().map((sensor, index) => (
                <div key={sensor.name} className="space-y-2 p-3 glass-card rounded-lg hover:bg-primary/5 transition-colors">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium">{sensor.name}</span>
                    </div>
                    <span className={`text-xs font-semibold ${sensor.risk === 'High' ? 'text-error' : sensor.risk === 'Medium' ? 'text-warning' : 'text-success'}`}>
                      {sensor.prediction}
                    </span>
                  </div>
                  <div className="text-xs text-muted-foreground">{sensor.location}</div>
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-muted-foreground">Confidence</span>
                    <span className="font-semibold">{sensor.confidence.toFixed(1)}%</span>
                  </div>
                  <Progress 
                    value={sensor.confidence} 
                    className={`h-1.5 ${sensor.risk === 'High' ? 'bg-error/20' : sensor.risk === 'Medium' ? 'bg-warning/20' : 'bg-success/20'}`} 
                  />
                </div>
              ))}
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>
    </div>
  );
};

export default DashboardSidebar;
