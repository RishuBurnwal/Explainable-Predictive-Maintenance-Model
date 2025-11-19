import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart, PieChart, Pie, Cell } from "recharts";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { TrendingUp, TrendingDown, Activity, AlertTriangle, RefreshCw, Database, Info } from "lucide-react";
import { useState, useEffect, useRef } from "react";
import PredictiveMaintenanceAPI, { generateSampleSensorData } from "@/lib/api";
import { TurbofanRecord, ensureDatasetAvailable, getRandomRecord, extractSensorData, getDatasetStats } from "@/lib/dataset";
import {
  Tooltip as UITooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from "@/components/ui/tooltip";

interface DataVisualizationProps {
  connectionStatus: 'checking' | 'connected' | 'disconnected';
  systemData: any;
  onDataRefresh: () => void;
}

// Simulated real-time data
const generateMockData = () => [
  { time: "00:00", rul: 95 + Math.random() * 5, anomaly: 0.1 + Math.random() * 0.05, temperature: 65 + Math.random() * 10 },
  { time: "04:00", rul: 92 + Math.random() * 5, anomaly: 0.15 + Math.random() * 0.05, temperature: 68 + Math.random() * 10 },
  { time: "08:00", rul: 88 + Math.random() * 5, anomaly: 0.2 + Math.random() * 0.05, temperature: 72 + Math.random() * 10 },
  { time: "12:00", rul: 85 + Math.random() * 5, anomaly: 0.25 + Math.random() * 0.05, temperature: 75 + Math.random() * 10 },
  { time: "16:00", rul: 78 + Math.random() * 5, anomaly: 0.4 + Math.random() * 0.05, temperature: 78 + Math.random() * 10 },
  { time: "20:00", rul: 72 + Math.random() * 5, anomaly: 0.55 + Math.random() * 0.05, temperature: 82 + Math.random() * 10 },
  { time: "24:00", rul: 68 + Math.random() * 5, anomaly: 0.7 + Math.random() * 0.05, temperature: 85 + Math.random() * 10 },
];

const getRiskDistribution = (systemData: any) => {
  if (systemData?.success && systemData.predictions) {
    // Try to extract risk probabilities from different possible data structures
    const riskData = systemData.predictions.failure_risk || systemData.predictions.risk;
    
    if (riskData?.probabilities) {
      const probs = riskData.probabilities;
      
      // Handle different probability formats
      let lowRisk = 0, medRisk = 0, highRisk = 0;
      
      if (typeof probs === 'object') {
        // Extract values regardless of key naming
        lowRisk = probs['Low Risk'] || probs['Low'] || probs.low || 0;
        medRisk = probs['Medium Risk'] || probs['Medium'] || probs.medium || 0;
        highRisk = probs['High Risk'] || probs['High'] || probs.high || 0;
      }
      
      // Normalize to percentages if needed
      const total = lowRisk + medRisk + highRisk;
      if (total > 0 && total <= 1) {
        // Probabilities are 0-1, convert to percentages
        lowRisk *= 100;
        medRisk *= 100;
        highRisk *= 100;
      }
      
      return [
        { name: 'Low Risk', value: Math.round(lowRisk), color: 'hsl(var(--success))' },
        { name: 'Medium Risk', value: Math.round(medRisk), color: 'hsl(var(--warning))' },
        { name: 'High Risk', value: Math.round(highRisk), color: 'hsl(var(--error))' }
      ];
    }
  }
  // Default/fallback distribution
  return [
    { name: 'Low Risk', value: 45, color: 'hsl(var(--success))' },
    { name: 'Medium Risk', value: 35, color: 'hsl(var(--warning))' },
    { name: 'High Risk', value: 20, color: 'hsl(var(--error))' }
  ];
};

const DataVisualization = ({ connectionStatus, systemData, onDataRefresh }: DataVisualizationProps) => {
  const api = new PredictiveMaintenanceAPI();
  const [data, setData] = useState(generateMockData());
  const [isLive, setIsLive] = useState(false);
  const [selectedMetric, setSelectedMetric] = useState<'rul' | 'anomaly' | 'temperature'>('rul');
  const [timeSeriesData, setTimeSeriesData] = useState<any[]>([]);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [dataset, setDataset] = useState<TurbofanRecord[]>([]);
  const [datasetStats, setDatasetStats] = useState<any>(null);
  const [isLoadingDataset, setIsLoadingDataset] = useState(false);
  const [useSensorData, setUseSensorData] = useState(false);
  
  // Refs to store previous values for comparison
  const prevSensorDataRef = useRef<any>(null);
  const prevSystemDataRef = useRef<any>(null);

  // Load dataset on component mount
  useEffect(() => {
    const loadDataset = async () => {
      if (connectionStatus === 'connected') {
        setIsLoadingDataset(true);
        try {
          const loadedDataset = await ensureDatasetAvailable('medium');
          setDataset(loadedDataset);
          setDatasetStats(getDatasetStats(loadedDataset));
        } catch (error) {
          console.error('Failed to load dataset:', error);
        }
        setIsLoadingDataset(false);
      }
    };

    loadDataset();
  }, [connectionStatus]);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isLive && connectionStatus === 'connected') {
      interval = setInterval(async () => {
        try {
          // Try to use real sensor data first
          try {
            const [sensorPredictions, realTimeSensors] = await Promise.all([
              api.getPredictionsFromSensors(),
              api.getAllSensors(true) // Get only active sensors
            ]);
            
            if (sensorPredictions.sensor_stats.active_sensors > 0) {
              setUseSensorData(true);
              
              // Calculate average temperature from actual temperature sensors
              const tempSensors = realTimeSensors.filter((s: any) => s.type === 'temperature');
              const avgTemp = tempSensors.length > 0 
                ? tempSensors.reduce((sum: number, s: any) => sum + s.current_value, 0) / tempSensors.length
                : 70;
              
              const newDataPoint = {
                time: new Date().toLocaleTimeString(),
                rul: sensorPredictions.predictions.rul?.value || 80,
                anomaly: Math.abs(sensorPredictions.predictions.anomaly?.score || 0.1),
                temperature: avgTemp,
                timestamp: Date.now()
              };
              
              // Only update if there are significant changes
              const prevDataPoint = timeSeriesData.length > 0 ? timeSeriesData[timeSeriesData.length - 1] : null;
              const shouldUpdate = !prevDataPoint || 
                Math.abs(newDataPoint.rul - prevDataPoint.rul) > 0.1 ||
                Math.abs(newDataPoint.anomaly - prevDataPoint.anomaly) > 0.001 ||
                Math.abs(newDataPoint.temperature - prevDataPoint.temperature) > 0.1;
              
              if (shouldUpdate) {
                setTimeSeriesData(prev => {
                  const updated = [...prev, newDataPoint].slice(-20);
                  return updated;
                });
                
                setData(prev => {
                  const newData = [...prev.slice(1), newDataPoint];
                  return newData;
                });
              }
              return;
            }
          } catch (sensorError) {
            console.log('Sensor data not available, using dataset');
          }
          
          // Fallback to dataset or sample data
          let sensorData: number[];
          if (dataset.length > 0) {
            const randomRecord = getRandomRecord(dataset);
            sensorData = randomRecord ? extractSensorData(randomRecord) : generateSampleSensorData();
          } else {
            sensorData = generateSampleSensorData();
          }
          
          const [rul, anomaly] = await Promise.all([
            api.predictRUL(sensorData, `MACHINE-LIVE-${Date.now()}`),
            api.detectAnomaly(sensorData, `MACHINE-LIVE-${Date.now()}`)
          ]);
          
          const newDataPoint = {
            time: new Date().toLocaleTimeString(),
            rul: rul.rul_prediction,
            anomaly: Math.abs(anomaly.anomaly_score),
            temperature: 65 + Math.random() * 20,
            timestamp: Date.now()
          };
          
          // Only update if there are significant changes
          const prevDataPoint = timeSeriesData.length > 0 ? timeSeriesData[timeSeriesData.length - 1] : null;
          const shouldUpdate = !prevDataPoint || 
            Math.abs(newDataPoint.rul - prevDataPoint.rul) > 0.1 ||
            Math.abs(newDataPoint.anomaly - prevDataPoint.anomaly) > 0.001 ||
            Math.abs(newDataPoint.temperature - prevDataPoint.temperature) > 0.1;
          
          if (shouldUpdate) {
            setTimeSeriesData(prev => {
              const updated = [...prev, newDataPoint].slice(-20);
              return updated;
            });
            
            setData(prev => {
              const newData = [...prev.slice(1), newDataPoint];
              return newData;
            });
          }
        } catch (error) {
          console.error('Live data update failed:', error);
          setData(generateMockData());
        }
      }, 3000);
    } else if (isLive) {
      interval = setInterval(() => {
        setData(generateMockData());
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [isLive, connectionStatus, dataset, timeSeriesData]);

  useEffect(() => {
    // Initialize with real data if available and if it has changed significantly
    if (systemData?.success && connectionStatus === 'connected') {
      // Check if systemData has changed significantly
      const hasChanged = !prevSystemDataRef.current || 
        JSON.stringify(systemData) !== JSON.stringify(prevSystemDataRef.current);
      
      if (hasChanged) {
        prevSystemDataRef.current = systemData;
        const { predictions } = systemData;
        const initialData = generateMockData().map((item, index) => ({
          ...item,
          rul: index === 6 ? (predictions.rul?.value || predictions.rul?.rul_prediction || item.rul) : item.rul,
          anomaly: index === 6 ? Math.abs(predictions.anomaly?.score || predictions.anomaly?.anomaly_score || item.anomaly) : item.anomaly
        }));
        setData(initialData);
      }
    }
  }, [systemData, connectionStatus]);

  const metricConfig = {
    rul: {
      title: "Remaining Useful Life (RUL)",
      description: "Predicted machine lifespan over time",
      color: "hsl(var(--primary))",
      unit: "hrs",
      icon: Activity
    },
    anomaly: {
      title: "Anomaly Score",
      description: "Detection of irregular patterns",
      color: "hsl(var(--warning))",
      unit: "",
      icon: AlertTriangle
    },
    temperature: {
      title: "Temperature Monitoring",
      description: "Thermal analysis and trending",
      color: "hsl(var(--error))",
      unit: "°C",
      icon: TrendingUp
    }
  };

  const currentMetric = metricConfig[selectedMetric];
  const riskDistribution = getRiskDistribution(systemData);
  
  const getQuickStats = () => {
    if (systemData?.success) {
      const { predictions } = systemData;
      const rulValue = predictions.rul?.value || predictions.rul?.rul_prediction || 82;
      const anomalyValue = predictions.anomaly?.score || predictions.anomaly?.anomaly_score || 0.1;
      return {
        avgRul: `${Math.round(rulValue)} hrs`,
        anomalies: Math.abs(anomalyValue).toFixed(2),
        tempAvg: `${Math.round(65 + Math.random() * 20)}°C` // Simulated temperature
      };
    }
    return {
      avgRul: "82.3 hrs",
      anomalies: "0.34",
      tempAvg: "76.2°C"
    };
  };
  
  const quickStats = getQuickStats();

  return (
    <div className="space-y-8">
      <div className="text-center space-y-4">
        <h2 className="text-3xl font-bold">Live Data Visualization</h2>
        <p className="text-muted-foreground">Real-time monitoring of machine health indicators</p>
        
        {/* Live Data Toggle and Controls */}
        <div className="flex justify-center items-center gap-4 flex-wrap">
          <Button
            variant={isLive ? "default" : "outline"}
            onClick={() => setIsLive(!isLive)}
            className="gap-2"
            disabled={connectionStatus === 'checking'}
          >
            <div className={`w-2 h-2 rounded-full ${
              isLive && connectionStatus === 'connected' 
                ? useSensorData ? 'bg-green-500 animate-pulse' : 'bg-success animate-pulse'
                : isLive 
                  ? 'bg-warning animate-pulse' 
                  : 'bg-muted-foreground'
            }`} />
            {isLive ? (connectionStatus === 'connected' ? (useSensorData ? 'Live Sensor Data' : 'Live Data') : 'Demo Mode') : 'Start Live Feed'}
          </Button>
          
          <Button
            variant="outline"
            onClick={async () => {
              setIsRefreshing(true);
              await onDataRefresh();
              setIsRefreshing(false);
            }}
            className="gap-2"
            disabled={connectionStatus !== 'connected' || isRefreshing}
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh Data
          </Button>

          {connectionStatus !== 'connected' && (
            <Badge variant="outline" className="gap-1">
              <AlertTriangle className="w-3 h-3" />
              {connectionStatus === 'checking' ? 'Connecting...' : 'Demo Mode'}
            </Badge>
          )}

          {connectionStatus === 'connected' && datasetStats && (
            <Badge variant="outline" className="gap-1">
              <Database className="w-3 h-3" />
              Dataset: {datasetStats.totalRecords} records, {datasetStats.uniqueEngines} engines
            </Badge>
          )}

          {isLoadingDataset && (
            <Badge variant="outline" className="gap-1">
              <div className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />
              Loading Dataset...
            </Badge>
          )}
          
          {/* Metric Selector */}
          <div className="flex gap-2">
            {Object.entries(metricConfig).map(([key, config]) => (
              <Badge
                key={key}
                variant={selectedMetric === key ? "default" : "outline"}
                className="cursor-pointer hover:scale-105 transition-transform"
                onClick={() => setSelectedMetric(key as typeof selectedMetric)}
              >
                <config.icon className="w-3 h-3 mr-1" />
                {config.title.split(' ')[0]}
              </Badge>
            ))}
          </div>
        </div>
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Main Chart */}
        <div className="lg:col-span-2">
          <Card className="glass-card card-3d group h-full">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <CardTitle className="flex items-center gap-2">
                    <currentMetric.icon className="w-5 h-5" />
                    {currentMetric.title}
                    <TooltipProvider>
                      <UITooltip>
                        <TooltipTrigger asChild>
                          <Info className="w-4 h-4 text-muted-foreground cursor-help hover:text-primary transition-colors" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="max-w-xs">{currentMetric.description}</p>
                          <p className="text-xs text-muted-foreground mt-1">
                            {selectedMetric === 'rul' && 'Tracks remaining operational hours before maintenance required'}
                            {selectedMetric === 'anomaly' && 'Monitors abnormal patterns indicating potential failures'}
                            {selectedMetric === 'temperature' && 'Real-time thermal monitoring from active temperature sensors'}
                          </p>
                        </TooltipContent>
                      </UITooltip>
                    </TooltipProvider>
                  </CardTitle>
                  <CardDescription>{currentMetric.description}</CardDescription>
                </div>
                <div className="flex items-center gap-2">
                  {isLive && (
                    <Badge variant="outline" className="animate-pulse">
                      <div className="w-2 h-2 bg-success rounded-full mr-2" />
                      Live
                    </Badge>
                  )}
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={async () => {
                      setIsRefreshing(true);
                      await onDataRefresh();
                      setIsRefreshing(false);
                    }}
                    disabled={connectionStatus !== 'connected' || isRefreshing}
                    title="Refresh chart data"
                  >
                    <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={350}>
                <AreaChart data={data}>
                  <defs>
                    <linearGradient id={`${selectedMetric}Gradient`} x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={currentMetric.color} stopOpacity={0.8}/>
                      <stop offset="95%" stopColor={currentMetric.color} stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis 
                    dataKey="time" 
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={12}
                  />
                  <YAxis 
                    stroke="hsl(var(--muted-foreground))"
                    fontSize={12}
                  />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                      boxShadow: "0 4px 6px -1px rgba(0, 0, 0, 0.1)"
                    }}
                    formatter={(value: number) => [
                      `${value.toFixed(1)}${currentMetric.unit}`,
                      currentMetric.title
                    ]}
                  />
                  <Area 
                    type="monotone" 
                    dataKey={selectedMetric}
                    stroke={currentMetric.color}
                    fill={`url(#${selectedMetric}Gradient)`}
                    strokeWidth={3}
                    dot={{ fill: currentMetric.color, r: 4 }}
                    activeDot={{ r: 6, stroke: currentMetric.color, strokeWidth: 2 }}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </div>

        {/* Risk Distribution */}
        <div className="space-y-6">
          <Card className="glass-card card-3d group">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <CardTitle className="flex items-center gap-2">
                    Risk Distribution
                    <TooltipProvider>
                      <UITooltip>
                        <TooltipTrigger asChild>
                          <Info className="w-4 h-4 text-muted-foreground cursor-help hover:text-primary transition-colors" />
                        </TooltipTrigger>
                        <TooltipContent>
                          <p className="max-w-xs">Distribution of risk levels across the production system based on AI predictions</p>
                        </TooltipContent>
                      </UITooltip>
                    </TooltipProvider>
                  </CardTitle>
                  <CardDescription>Current system risk levels</CardDescription>
                </div>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={async () => {
                    setIsRefreshing(true);
                    await onDataRefresh();
                    setIsRefreshing(false);
                  }}
                  disabled={connectionStatus !== 'connected' || isRefreshing}
                  title="Refresh risk data"
                >
                  <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={riskDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {riskDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: "hsl(var(--card))",
                      border: "1px solid hsl(var(--border))",
                      borderRadius: "8px",
                    }}
                    formatter={(value: number) => [`${value}%`, 'Machines']}
                  />
                </PieChart>
              </ResponsiveContainer>
              
              <div className="space-y-2 mt-4">
                {riskDistribution.map((item) => (
                  <div key={item.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div 
                        className="w-3 h-3 rounded-full" 
                        style={{ backgroundColor: item.color }}
                      />
                      <span className="text-sm">{item.name}</span>
                    </div>
                    <span className="text-sm font-medium">{item.value}%</span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Quick Stats */}
          <Card className="glass-card card-3d group">
            <CardHeader>
              <CardTitle>Quick Stats</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Avg RUL</span>
                <div className="flex items-center gap-1">
                  <TrendingDown className="w-4 h-4 text-error" />
                  <span className="font-medium">{quickStats.avgRul}</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Anomalies</span>
                <div className="flex items-center gap-1">
                  <TrendingUp className="w-4 h-4 text-warning" />
                  <span className="font-medium">{quickStats.anomalies}</span>
                </div>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Temp Avg</span>
                <div className="flex items-center gap-1">
                  <TrendingUp className="w-4 h-4 text-error" />
                  <span className="font-medium">{quickStats.tempAvg}</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default DataVisualization;