import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from "recharts";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Info, Brain, Target, Lightbulb, TrendingUp, AlertTriangle, RefreshCw } from "lucide-react";
import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Tooltip as UITooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";
import { ensureDatasetAvailable, getRandomRecord, extractSensorData, TurbofanRecord } from "@/lib/dataset";

interface ExplainabilityPanelProps {
  connectionStatus: 'checking' | 'connected' | 'disconnected';
  systemData: any;
}

const shapData = [
  { feature: "Temperature", impact: 0.85, positive: true, description: "High temperature increases failure risk" },
  { feature: "Vibration", impact: 0.72, positive: true, description: "Excessive vibration indicates mechanical stress" },
  { feature: "Pressure", impact: 0.58, positive: false, description: "Lower pressure reduces system efficiency" },
  { feature: "RPM", impact: 0.45, positive: true, description: "High RPM accelerates component wear" },
  { feature: "Load", impact: 0.32, positive: true, description: "Heavy load increases operational stress" },
  { feature: "Humidity", impact: 0.28, positive: true, description: "High humidity affects electrical components" },
];

const radarData = [
  { subject: 'Thermal', A: 120, B: 110, fullMark: 150 },
  { subject: 'Mechanical', A: 98, B: 130, fullMark: 150 },
  { subject: 'Electrical', A: 86, B: 130, fullMark: 150 },
  { subject: 'Operational', A: 99, B: 100, fullMark: 150 },
  { subject: 'Environmental', A: 85, B: 90, fullMark: 150 },
];

const ExplainabilityPanel = ({ connectionStatus, systemData }: ExplainabilityPanelProps) => {
  const [selectedFeature, setSelectedFeature] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState("shap");
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [dataset, setDataset] = useState<TurbofanRecord[]>([]);
  const [currentRecord, setCurrentRecord] = useState<TurbofanRecord | null>(null);
  const [limeData, setLimeData] = useState([
    { feature: "Temperature", local: 0.92, global: 0.85, index: 0 },
    { feature: "Vibration", local: 0.68, global: 0.72, index: 1 },
    { feature: "Pressure", local: 0.45, global: 0.58, index: 2 },
    { feature: "RPM", local: 0.38, global: 0.45, index: 3 },
    { feature: "Load", local: 0.25, global: 0.32, index: 4 },
    { feature: "Humidity", local: 0.15, global: 0.28, index: 5 },
  ]);

  // Load offline dataset on mount
  useEffect(() => {
    const loadDataset = async () => {
      try {
        const data = await ensureDatasetAvailable('medium');
        setDataset(data);
        
        // Get initial random record
        const record = getRandomRecord(data);
        if (record) {
          setCurrentRecord(record);
          updateLimeDataFromRecord(record);
        }
      } catch (error) {
        console.error('Failed to load dataset:', error);
      }
    };
    
    loadDataset();
  }, []);

  // Update LIME data based on actual sensor record
  const updateLimeDataFromRecord = (record: TurbofanRecord) => {
    const sensorData = extractSensorData(record);
    
    // Calculate local importance based on actual sensor values
    // Normalize values and calculate variance-based importance
    const normalized = sensorData.map((val, idx) => {
      if (idx < 3) return Math.abs(val); // Operational settings
      return val / 1000; // Normalize sensor values
    });
    
    // Map important sensors to features
    const featureMapping = [
      { name: "Temperature", indices: [3, 4, 11, 12], global: 0.85 },
      { name: "Vibration", indices: [6, 7, 8], global: 0.72 },
      { name: "Pressure", indices: [2, 10, 13], global: 0.58 },
      { name: "RPM", indices: [8, 9, 14], global: 0.45 },
      { name: "Load", indices: [0, 1, 5], global: 0.32 },
      { name: "Humidity", indices: [15, 16, 17], global: 0.28 },
    ];
    
    const updatedLime = featureMapping.map((feature, idx) => {
      // Calculate local importance from actual sensor values
      const localValues = feature.indices.map(i => normalized[i] || 0);
      const localImportance = localValues.reduce((sum, val) => sum + Math.abs(val), 0) / localValues.length;
      
      return {
        feature: feature.name,
        local: Math.min(localImportance, 1),
        global: feature.global,
        index: idx
      };
    });
    
    setLimeData(updatedLime);
  };

  const getFeatureColor = (positive: boolean) => positive ? "hsl(var(--error))" : "hsl(var(--success))";

  // Use SHAP data for visualization
  const currentShapData = shapData;

  const handleRefresh = async () => {
    setIsRefreshing(true);
    
    // Get new random record from offline dataset
    if (dataset.length > 0) {
      const newRecord = getRandomRecord(dataset);
      if (newRecord) {
        setCurrentRecord(newRecord);
        updateLimeDataFromRecord(newRecord);
      }
    }
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    setIsRefreshing(false);
  };

  return (
    <section className="space-y-8">
      <div className="text-center space-y-4">
        <h2 className="text-3xl font-bold">AI Explainability Insights</h2>
        <p className="text-muted-foreground">Understanding the factors behind predictions with transparent AI</p>
        
        <div className="flex justify-center gap-2 flex-wrap">
          <Badge variant="outline" className="gap-1">
            <Brain className="w-3 h-3" />
            SHAP Analysis
          </Badge>
          <Badge variant="outline" className="gap-1">
            <Target className="w-3 h-3" />
            LIME Explanations
          </Badge>
          <Badge variant="outline" className="gap-1">
            <Lightbulb className="w-3 h-3" />
            Feature Impact
          </Badge>
          
          {connectionStatus !== 'connected' && (
            <Badge variant="outline" className="gap-1">
              <AlertTriangle className="w-3 h-3" />
              {connectionStatus === 'checking' ? 'Loading...' : 'Demo Data'}
            </Badge>
          )}
        </div>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="grid w-full grid-cols-3 max-w-md mx-auto">
          <TabsTrigger value="shap" className="gap-2">
            <Brain className="w-4 h-4" />
            SHAP
          </TabsTrigger>
          <TabsTrigger value="lime" className="gap-2">
            <Target className="w-4 h-4" />
            LIME
          </TabsTrigger>
          <TabsTrigger value="radar" className="gap-2">
            <TrendingUp className="w-4 h-4" />
            Overview
          </TabsTrigger>
        </TabsList>

        <div className="mt-8">
          <TabsContent value="shap" className="space-y-6">
            <div className="grid lg:grid-cols-3 gap-6">
              {/* SHAP Feature Importance */}
              <div className="lg:col-span-2">
                <Card className="glass-card card-3d group h-full">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <div className="flex-1">
                        <CardTitle className="flex items-center gap-2">
                          <Brain className="w-5 h-5 text-primary" />
                          SHAP Feature Importance
                          <TooltipProvider>
                            <UITooltip>
                              <TooltipTrigger asChild>
                                <Info className="w-4 h-4 text-muted-foreground cursor-help hover:text-primary transition-colors" />
                              </TooltipTrigger>
                              <TooltipContent>
                                <p className="max-w-xs">SHAP (SHapley Additive exPlanations) values show how much each feature contributes to the model's predictions</p>
                              </TooltipContent>
                            </UITooltip>
                          </TooltipProvider>
                        </CardTitle>
                        <CardDescription>Global feature impact on failure predictions</CardDescription>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={handleRefresh}
                        disabled={isRefreshing}
                        title="Refresh SHAP analysis"
                      >
                        <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={400}>
                      <BarChart data={currentShapData} layout="vertical" margin={{ left: 80 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                        <XAxis type="number" stroke="hsl(var(--muted-foreground))" />
                        <YAxis 
                          dataKey="feature" 
                          type="category" 
                          stroke="hsl(var(--muted-foreground))"
                          width={80}
                        />
                        <Tooltip 
                          contentStyle={{
                            backgroundColor: "hsl(var(--card))",
                            border: "1px solid hsl(var(--border))",
                            borderRadius: "8px",
                            boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
                          }}
                          formatter={(value: number, name, props) => [
                            `${(value * 100).toFixed(1)}%`,
                            'Impact Score',
                            props.payload.description
                          ]}
                        />
                        <Bar 
                          dataKey="impact" 
                          fill="hsl(var(--primary))"
                          radius={[0, 8, 8, 0]}
                          onClick={(data: any) => setSelectedFeature(data.feature)}
                          className="cursor-pointer hover:opacity-80 transition-opacity"
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </CardContent>
                </Card>
              </div>

              {/* Feature Details */}
              <div>
                <Card className="glass-card card-3d group h-full">
                  <CardHeader>
                    <CardTitle>Feature Analysis</CardTitle>
                    <CardDescription>
                      {selectedFeature ? `Details for ${selectedFeature}` : 'Click a feature to explore'}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    {selectedFeature ? (
                      <>
                        {currentShapData
                          .filter(item => item.feature === selectedFeature)
                          .map(item => (
                            <div key={item.feature} className="space-y-3">
                              <div className="flex items-center justify-between">
                                <span className="font-medium">{item.feature}</span>
                                <Badge variant={item.positive ? "destructive" : "default"}>
                                  {item.positive ? 'Risk Factor' : 'Protective'}
                                </Badge>
                              </div>
                              
                              <div className="space-y-2">
                                <div className="flex justify-between text-sm">
                                  <span>Impact Score</span>
                                  <span className="font-medium">{(item.impact * 100).toFixed(1)}%</span>
                                </div>
                                <div className="w-full bg-muted rounded-full h-2">
                                  <div 
                                    className="h-2 rounded-full bg-primary"
                                    style={{ width: `${item.impact * 100}%` }}
                                  />
                                </div>
                              </div>
                              
                              <p className="text-sm text-muted-foreground">
                                {item.description}
                              </p>
                            </div>
                          ))}
                      </>
                    ) : (
                      <div className="text-center py-8 text-muted-foreground">
                        <Brain className="w-12 h-12 mx-auto mb-4 opacity-50" />
                        <p>Select a feature from the chart to see detailed analysis</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="lime" className="space-y-6">
            <Card className="glass-card card-3d group">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <CardTitle className="flex items-center gap-2">
                      <Target className="w-5 h-5 text-primary" />
                      LIME Local vs Global Explanations
                      <TooltipProvider>
                        <UITooltip>
                          <TooltipTrigger asChild>
                            <Info className="w-4 h-4 text-muted-foreground cursor-help hover:text-primary transition-colors" />
                          </TooltipTrigger>
                          <TooltipContent>
                            <p className="max-w-xs">LIME (Local Interpretable Model-agnostic Explanations) compares instance-specific predictions with global patterns</p>
                          </TooltipContent>
                        </UITooltip>
                      </TooltipProvider>
                    </CardTitle>
                    <CardDescription>
                      Comparing local instance explanations with global model behavior
                      {currentRecord && (
                        <Badge variant="outline" className="ml-2">
                          Engine #{currentRecord.unit_number} Cycle {currentRecord.time_cycles}
                        </Badge>
                      )}
                    </CardDescription>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={handleRefresh}
                    disabled={isRefreshing}
                    title="Refresh LIME analysis"
                  >
                    <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={limeData} margin={{ left: 80 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                    <XAxis stroke="hsl(var(--muted-foreground))" />
                    <YAxis 
                      dataKey="feature" 
                      type="category" 
                      stroke="hsl(var(--muted-foreground))"
                      width={80}
                    />
                    <Tooltip 
                      contentStyle={{
                        backgroundColor: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "8px",
                      }}
                    />
                    <Bar 
                      dataKey="local" 
                      fill="hsl(var(--primary))"
                      name="Local Explanation"
                      radius={[0, 4, 4, 0]}
                    />
                    <Bar 
                      dataKey="global" 
                      fill="hsl(var(--warning))"
                      name="Global Importance"
                      radius={[0, 4, 4, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
                
                <div className="mt-6 p-4 glass-card rounded-lg">
                  <div className="flex items-center gap-4 mb-3">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-primary rounded" />
                      <span className="text-sm">Local Instance</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-warning rounded" />
                      <span className="text-sm">Global Model</span>
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    <span className="text-primary font-semibold">Local Analysis:</span> For this specific machine instance, 
                    temperature has an even higher impact (92%) compared to the global model average (85%). 
                    This suggests this particular machine is more sensitive to thermal conditions.
                  </p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="radar" className="space-y-6">
            <Card className="glass-card card-3d group">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="w-5 h-5 text-primary" />
                      Multi-Dimensional Risk Assessment
                      <TooltipProvider>
                        <UITooltip>
                          <TooltipTrigger asChild>
                            <Info className="w-4 h-4 text-muted-foreground cursor-help hover:text-primary transition-colors" />
                          </TooltipTrigger>
                          <TooltipContent>
                            <p className="max-w-xs">Radar chart visualizes risk levels across multiple categories simultaneously</p>
                          </TooltipContent>
                        </UITooltip>
                      </TooltipProvider>
                    </CardTitle>
                    <CardDescription>
                      Comprehensive view of risk factors across different categories
                    </CardDescription>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={handleRefresh}
                    disabled={isRefreshing}
                    title="Refresh risk assessment"
                  >
                    <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={400}>
                  <RadarChart data={radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" />
                    <PolarRadiusAxis angle={90} domain={[0, 150]} />
                    <Radar
                      name="Current State"
                      dataKey="A"
                      stroke="hsl(var(--primary))"
                      fill="hsl(var(--primary))"
                      fillOpacity={0.3}
                      strokeWidth={2}
                    />
                    <Radar
                      name="Threshold"
                      dataKey="B"
                      stroke="hsl(var(--warning))"
                      fill="hsl(var(--warning))"
                      fillOpacity={0.1}
                      strokeWidth={2}
                    />
                    <Tooltip 
                      contentStyle={{
                        backgroundColor: "hsl(var(--card))",
                        border: "1px solid hsl(var(--border))",
                        borderRadius: "8px",
                      }}
                    />
                  </RadarChart>
                </ResponsiveContainer>
                
                <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-6">
                  {radarData.map((item, index) => (
                    <div key={item.subject} className="text-center p-3 glass-card rounded-lg">
                      <div className="text-lg font-bold text-primary">{item.A}</div>
                      <div className="text-xs text-muted-foreground">{item.subject}</div>
                      <div className="text-xs text-warning">/{item.B}</div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </div>
      </Tabs>
    </section>
  );
};

export default ExplainabilityPanel;
