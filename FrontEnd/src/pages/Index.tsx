import Navigation from "@/components/Navigation";
import Hero from "@/components/Hero";
import StatusCard from "@/components/StatusCard";
import DataVisualization from "@/components/DataVisualization";
import ExplainabilityPanel from "@/components/ExplainabilityPanel";
import AlertCard from "@/components/AlertCard";
import DashboardSidebar from "@/components/DashboardSidebar";
import { Activity, Gauge, AlertTriangle, CheckCircle, RefreshCw, Clock } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Card, CardContent } from "@/components/ui/card";
import { useState, useEffect } from "react";
import PredictiveMaintenanceAPI, { generateSampleSensorData } from "@/lib/api";

const Index = () => {
  const api = new PredictiveMaintenanceAPI();
  const [systemData, setSystemData] = useState<any>(null);
  const [connectionStatus, setConnectionStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');
  const [isLoading, setIsLoading] = useState(true);
  const [useSensorData, setUseSensorData] = useState(false);
  const [refreshInterval, setRefreshInterval] = useState<number>(15); // Default 15 seconds
  const [systemStartTime, setSystemStartTime] = useState<number>(() => {
    // Check if we have a stored start time
    const storedStartTime = localStorage.getItem('systemStartTime');
    if (storedStartTime) {
      return parseInt(storedStartTime, 10);
    }
    // Otherwise, set and store the current time
    const now = Date.now();
    localStorage.setItem('systemStartTime', now.toString());
    return now;
  });
  const [uptime, setUptime] = useState<string>('0h 0m');
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Calculate system uptime
  useEffect(() => {
    const calculateUptime = () => {
      const now = Date.now();
      const diff = now - systemStartTime;
      
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      const seconds = Math.floor((diff % (1000 * 60)) / 1000);
      
      setUptime(`${hours}h ${minutes}m ${seconds}s`);
    };
    
    calculateUptime();
    const interval = setInterval(calculateUptime, 1000);
    
    return () => clearInterval(interval);
  }, [systemStartTime]);

  useEffect(() => {
    const initializeSystem = async () => {
      setIsLoading(true);
      
      // Test connection
      const connection = await api.testConnection();
      setConnectionStatus(connection.connected ? 'connected' : 'disconnected');
      
      if (connection.connected) {
        // Try to get sensor-based predictions first
        try {
          const sensorPredictions = await api.getPredictionsFromSensors();
          if (sensorPredictions.sensor_stats.active_sensors > 0) {
            setUseSensorData(true);
            setSystemData({
              success: true,
              predictions: {
                rul: sensorPredictions.predictions.rul,
                risk: {
                  risk_class: sensorPredictions.predictions.failure_risk?.class || 'Medium',
                  risk_probabilities: sensorPredictions.predictions.failure_risk?.probabilities || { Low: 0.3, Medium: 0.5, High: 0.2 },
                  risk_score: sensorPredictions.predictions.failure_risk?.confidence || 0.7
                },
                anomaly: {
                  is_anomaly: sensorPredictions.predictions.anomaly?.is_anomaly || false,
                  anomaly_score: sensorPredictions.predictions.anomaly?.score || 0.1,
                  severity: sensorPredictions.predictions.anomaly?.is_anomaly ? 'High' : 'Low'
                }
              },
              sensor_stats: sensorPredictions.sensor_stats
            });
          } else {
            // Fallback to sample data if no sensors active
            const sensorData = generateSampleSensorData();
            const predictions = await api.getCompletePrediction(sensorData, 'MACHINE-001');
            setSystemData(predictions);
          }
        } catch (error) {
          console.error('Failed to get sensor predictions, using sample data:', error);
          const sensorData = generateSampleSensorData();
          const predictions = await api.getCompletePrediction(sensorData, 'MACHINE-001');
          setSystemData(predictions);
        }
      }
      
      setIsLoading(false);
    };

    initializeSystem();
    
    // Set up periodic updates with configurable interval
    if (refreshInterval === 0) {
      // Real-time mode: continuous updates with requestAnimationFrame
      let isRunning = true;
      
      const realtimeUpdate = async () => {
        if (!isRunning || connectionStatus !== 'connected') return;
        
        try {
          if (useSensorData) {
            const sensorPredictions = await api.getPredictionsFromSensors();
            setSystemData({
              success: true,
              predictions: {
                rul: sensorPredictions.predictions.rul,
                risk: {
                  risk_class: sensorPredictions.predictions.failure_risk?.class || 'Medium',
                  risk_probabilities: sensorPredictions.predictions.failure_risk?.probabilities || { Low: 0.3, Medium: 0.5, High: 0.2 },
                  risk_score: sensorPredictions.predictions.failure_risk?.confidence || 0.7
                },
                anomaly: {
                  is_anomaly: sensorPredictions.predictions.anomaly?.is_anomaly || false,
                  anomaly_score: sensorPredictions.predictions.anomaly?.score || 0.1,
                  severity: sensorPredictions.predictions.anomaly?.is_anomaly ? 'High' : 'Low'
                }
              },
              sensor_stats: sensorPredictions.sensor_stats
            });
          } else {
            const sensorData = generateSampleSensorData();
            const predictions = await api.getCompletePrediction(sensorData, 'MACHINE-001');
            setSystemData(predictions);
          }
        } catch (error) {
          console.error('Real-time update failed:', error);
        }
        
        // Schedule next update immediately
        if (isRunning) {
          setTimeout(realtimeUpdate, 100); // Minimal delay for browser performance
        }
      };
      
      realtimeUpdate();
      
      return () => {
        isRunning = false;
      };
    } else {
      // Interval-based updates
      const interval = setInterval(async () => {
      if (connectionStatus === 'connected') {
        try {
          if (useSensorData) {
            // Use real sensor data
            const sensorPredictions = await api.getPredictionsFromSensors();
            setSystemData({
              success: true,
              predictions: {
                rul: sensorPredictions.predictions.rul,
                risk: {
                  risk_class: sensorPredictions.predictions.failure_risk?.class || 'Medium',
                  risk_probabilities: sensorPredictions.predictions.failure_risk?.probabilities || { Low: 0.3, Medium: 0.5, High: 0.2 },
                  risk_score: sensorPredictions.predictions.failure_risk?.confidence || 0.7
                },
                anomaly: {
                  is_anomaly: sensorPredictions.predictions.anomaly?.is_anomaly || false,
                  anomaly_score: sensorPredictions.predictions.anomaly?.score || 0.1,
                  severity: sensorPredictions.predictions.anomaly?.is_anomaly ? 'High' : 'Low'
                }
              },
              sensor_stats: sensorPredictions.sensor_stats
            });
          } else {
            // Use sample data
            const sensorData = generateSampleSensorData();
            const predictions = await api.getCompletePrediction(sensorData, 'MACHINE-001');
            setSystemData(predictions);
          }
        } catch (error) {
          console.error('Update failed:', error);
        }
      }
      }, refreshInterval * 1000); // Convert to milliseconds

      return () => clearInterval(interval);
    }
  }, [connectionStatus, useSensorData, refreshInterval]);

  // Reset system uptime
  const handleResetUptime = () => {
    const now = Date.now();
    localStorage.setItem('systemStartTime', now.toString());
    setSystemStartTime(now);
  };

  // Manual refresh function
  const handleManualRefresh = async () => {
    setIsRefreshing(true);
    try {
      if (connectionStatus === 'connected') {
        if (useSensorData) {
          const sensorPredictions = await api.getPredictionsFromSensors();
          setSystemData({
            success: true,
            predictions: {
              rul: sensorPredictions.predictions.rul,
              risk: {
                risk_class: sensorPredictions.predictions.failure_risk?.class || 'Medium',
                risk_probabilities: sensorPredictions.predictions.failure_risk?.probabilities || {},
                risk_score: sensorPredictions.predictions.failure_risk?.confidence || 0.7
              },
              anomaly: {
                is_anomaly: sensorPredictions.predictions.anomaly?.is_anomaly || false,
                anomaly_score: sensorPredictions.predictions.anomaly?.score || 0.1,
                severity: sensorPredictions.predictions.anomaly?.is_anomaly ? 'High' : 'Low'
              }
            },
            sensor_stats: sensorPredictions.sensor_stats
          });
        } else {
          const sensorData = generateSampleSensorData();
          const predictions = await api.getCompletePrediction(sensorData, 'MACHINE-001');
          setSystemData(predictions);
        }
      }
    } catch (error) {
      console.error('Manual refresh failed:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  const getStatusCardData = () => {
    if (!systemData?.success || !systemData?.predictions) {
      // Show demo/fallback data instead of loading states
      return {
        engineStatus: { 
          value: connectionStatus === 'connected' ? "Running" : connectionStatus === 'checking' ? "Connecting..." : "Demo Mode", 
          status: connectionStatus === 'connected' ? "success" as const : connectionStatus === 'checking' ? "warning" as const : "info" as const, 
          description: connectionStatus === 'connected' ? "All systems operational" : connectionStatus === 'checking' ? "Establishing connection" : "Running in demonstration mode", 
          trend: "stable" as const, 
          percentage: "100%" 
        },
        rulPrediction: { 
          value: connectionStatus === 'checking' ? "Loading..." : "Calculating...", 
          status: "success" as const, 
          description: connectionStatus === 'checking' ? "Initializing model..." : "Waiting for sensor data", 
          trend: "down" as const, 
          percentage: "0%" 
        },
        riskLevel: { 
          value: connectionStatus === 'checking' ? "Analyzing..." : "Medium", 
          status: connectionStatus === 'checking' ? "warning" as const : "warning" as const, 
          description: connectionStatus === 'checking' ? "Processing risk assessment" : "Demo risk assessment", 
          trend: "stable" as const, 
          percentage: "35%" 
        },
        anomalyStatus: { 
          value: connectionStatus === 'checking' ? "Scanning..." : "Normal", 
          status: connectionStatus === 'checking' ? "warning" as const : "success" as const, 
          description: connectionStatus === 'checking' ? "Anomaly detection initializing" : "No anomalies detected (demo)", 
          trend: "stable" as const, 
          percentage: "5%" 
        }
      };
    }

    const { predictions } = systemData;
    
    // Extract RUL data
    const rulValue = predictions.rul?.value ?? predictions.rul?.rul_prediction ?? 0;
    const rulRiskLevel = predictions.rul?.risk_level ?? 'Low';
    const rulConfidence = predictions.rul?.confidence ?? 0.8;
    
    // Extract risk data
    const riskClass = predictions.risk?.risk_class ?? predictions.failure_risk?.class ?? 'Low Risk';
    const riskProbs = predictions.risk?.risk_probabilities ?? predictions.failure_risk?.probabilities ?? { 'Low Risk': 0.8, 'Medium Risk': 0.15, 'High Risk': 0.05 };
    const riskScore = predictions.risk?.risk_score ?? predictions.failure_risk?.confidence ?? 0.3;
    
    // Extract anomaly data
    const isAnomaly = predictions.anomaly?.is_anomaly ?? false;
    const anomalyScore = predictions.anomaly?.anomaly_score ?? predictions.anomaly?.score ?? 0.1;
    const anomalySeverity = predictions.anomaly?.severity ?? (isAnomaly ? 'High' : 'Low');

    return {
      engineStatus: {
        value: systemData?.sensor_stats ? `${systemData.sensor_stats.active_sensors} Sensors Active` : "Running",
        status: (systemData?.sensor_stats?.critical_sensors ?? 0) > 0 ? "error" as const : 
                (systemData?.sensor_stats?.warning_sensors ?? 0) > 0 ? "warning" as const : "success" as const,
        description: systemData?.sensor_stats ? 
          `${systemData.sensor_stats.critical_sensors} critical, ${systemData.sensor_stats.warning_sensors} warning` :
          "All systems operational",
        trend: "stable" as const,
        percentage: systemData?.sensor_stats ? `${systemData.sensor_stats.health_score}%` : "100%"
      },
      rulPrediction: {
        value: rulValue > 0 ? `${Math.round(rulValue)} hrs` : "N/A",
        status: rulRiskLevel === 'High' ? "error" as const : rulRiskLevel === 'Medium' ? "warning" as const : "success" as const,
        description: `Confidence: ${Math.round(rulConfidence * 100)}%`,
        trend: rulRiskLevel === 'High' ? "down" as const : "stable" as const,
        percentage: `${Math.round((1 - rulConfidence) * 100)}%`
      },
      riskLevel: {
        value: riskClass,
        status: riskClass.includes('High') ? "error" as const : riskClass.includes('Medium') ? "warning" as const : "success" as const,
        description: `Risk Score: ${riskScore.toFixed(2)}`,
        trend: riskClass.includes('High') ? "up" as const : "stable" as const,
        percentage: `${Math.round((riskProbs[riskClass] ?? riskScore) * 100)}%`
      },
      anomalyStatus: {
        value: isAnomaly ? `${anomalySeverity} Risk` : "Normal",
        status: isAnomaly ? (anomalySeverity === 'High' ? "error" as const : "warning" as const) : "success" as const,
        description: isAnomaly ? `Score: ${Math.abs(anomalyScore).toFixed(3)}` : "No anomalies detected",
        trend: isAnomaly ? "up" as const : "stable" as const,
        percentage: `${Math.round(Math.abs(anomalyScore) * 100)}%`
      }
    };
  };

  const statusData = getStatusCardData();

  return (
    <div className="min-h-screen">
      <Navigation />
      <div id="home">
        <Hero />
      </div>
      
      <div className="container mx-auto px-4 py-16">
        {/* Refresh Interval Control Bar */}
        <Card className="glass-card mb-8">
          <CardContent className="py-4">
            <div className="flex flex-wrap items-center justify-between gap-4">
              {/* System Uptime */}
              <div className="flex items-center gap-3">
                <Clock className="w-5 h-5 text-primary" />
                <div>
                  <p className="text-sm font-medium">System Uptime</p>
                  <p className="text-lg font-bold text-primary">{uptime}</p>
                </div>
              </div>
              
              {/* Refresh Interval Selector */}
              <div className="flex items-center gap-3">
                <RefreshCw className="w-5 h-5 text-primary" />
                <div className="flex items-center gap-2">
                  <label className="text-sm font-medium whitespace-nowrap">Update Interval:</label>
                  <Select
                    value={refreshInterval.toString()}
                    onValueChange={(value) => setRefreshInterval(Number(value))}
                  >
                    <SelectTrigger className="w-[180px]">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="0">Real-time (Instant)</SelectItem>
                      <SelectItem value="5">5 seconds</SelectItem>
                      <SelectItem value="10">10 seconds</SelectItem>
                      <SelectItem value="15">15 seconds</SelectItem>
                      <SelectItem value="30">30 seconds</SelectItem>
                      <SelectItem value="60">1 minute</SelectItem>
                      <SelectItem value="120">2 minutes</SelectItem>
                      <SelectItem value="300">5 minutes</SelectItem>
                      <SelectItem value="600">10 minutes</SelectItem>
                      <SelectItem value="900">15 minutes</SelectItem>
                      <SelectItem value="1800">30 minutes</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
              
              {/* Manual Refresh Button */}
              <div className="flex gap-2">
                <Button
                  onClick={handleManualRefresh}
                  disabled={isRefreshing || connectionStatus !== 'connected'}
                  className="gap-2"
                >
                  <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
                  {isRefreshing ? 'Refreshing...' : 'Refresh Now'}
                </Button>
                <Button
                  onClick={handleResetUptime}
                  variant="outline"
                  className="gap-2"
                >
                  <Clock className="w-4 h-4" />
                  Reset Uptime
                </Button>
              </div>
              
              {/* Connection Status Badge */}
              <Badge
                variant={connectionStatus === 'connected' ? 'default' : connectionStatus === 'checking' ? 'secondary' : 'destructive'}
                className="gap-1"
              >
                {connectionStatus === 'connected' && <CheckCircle className="w-3 h-3" />}
                {connectionStatus === 'checking' && <div className="w-3 h-3 border border-current border-t-transparent rounded-full animate-spin" />}
                {connectionStatus === 'disconnected' && <AlertTriangle className="w-3 h-3" />}
                {connectionStatus === 'connected' ? 'Connected' : connectionStatus === 'checking' ? 'Connecting' : 'Disconnected'}
              </Badge>
            </div>
          </CardContent>
        </Card>
        
        <div className="grid lg:grid-cols-4 gap-8">
          <div className="lg:col-span-3 space-y-16">
            {/* Status Cards Section */}
            <section id="dashboard" className="space-y-6 animate-fade-in">
              <div className="text-center space-y-2">
                <h2 className="text-3xl font-bold">Real-Time System Status</h2>
                <p className="text-muted-foreground">
                  {useSensorData 
                    ? `Live monitoring from ${systemData?.sensor_stats?.active_sensors || 0} active sensors` 
                    : "Live monitoring of critical machine health indicators"}
                </p>
                {connectionStatus === 'checking' && (
                  <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
                    <div className="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
                    Connecting to backend...
                  </div>
                )}
                {connectionStatus === 'disconnected' && (
                  <div className="flex items-center justify-center gap-2 text-sm text-destructive">
                    <AlertTriangle className="w-4 h-4" />
                    Backend connection failed - showing demo data
                  </div>
                )}
                {connectionStatus === 'connected' && (
                  <div className="flex items-center justify-center gap-2 text-sm text-success">
                    <CheckCircle className="w-4 h-4" />
                    {useSensorData 
                      ? `Connected - Using ${systemData?.sensor_stats?.active_sensors || 0} Real Sensors` 
                      : "Connected to live backend"}
                  </div>
                )}
              </div>
              
              <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatusCard
                  title="Engine Status"
                  value={statusData.engineStatus.value}
                  icon={Activity}
                  status={statusData.engineStatus.status}
                  description={statusData.engineStatus.description}
                  trend={statusData.engineStatus.trend}
                  percentage={statusData.engineStatus.percentage}
                />
                <StatusCard
                  title="RUL Prediction"
                  value={statusData.rulPrediction.value}
                  icon={Gauge}
                  status={statusData.rulPrediction.status}
                  description={statusData.rulPrediction.description}
                  trend={statusData.rulPrediction.trend}
                  percentage={statusData.rulPrediction.percentage}
                />
                <StatusCard
                  title="Risk Level"
                  value={statusData.riskLevel.value}
                  icon={AlertTriangle}
                  status={statusData.riskLevel.status}
                  description={statusData.riskLevel.description}
                  trend={statusData.riskLevel.trend}
                  percentage={statusData.riskLevel.percentage}
                />
                <StatusCard
                  title="Anomaly Status"
                  value={statusData.anomalyStatus.value}
                  icon={AlertTriangle}
                  status={statusData.anomalyStatus.status}
                  description={statusData.anomalyStatus.description}
                  trend={statusData.anomalyStatus.trend}
                  percentage={statusData.anomalyStatus.percentage}
                />
              </div>
            </section>

            {/* Data Visualization */}
            <section id="visualizations">
              <DataVisualization 
                connectionStatus={connectionStatus}
                systemData={systemData}
                onDataRefresh={async () => {
                  if (connectionStatus === 'connected') {
                    try {
                      if (useSensorData) {
                        const sensorPredictions = await api.getPredictionsFromSensors();
                        setSystemData({
                          success: true,
                          predictions: {
                            rul: sensorPredictions.predictions.rul,
                            risk: {
                              risk_class: sensorPredictions.predictions.failure_risk?.class || 'Medium',
                              risk_probabilities: sensorPredictions.predictions.failure_risk?.probabilities || {},
                              risk_score: sensorPredictions.predictions.failure_risk?.confidence || 0.7
                            },
                            anomaly: {
                              is_anomaly: sensorPredictions.predictions.anomaly?.is_anomaly || false,
                              anomaly_score: sensorPredictions.predictions.anomaly?.score || 0.1,
                              severity: sensorPredictions.predictions.anomaly?.is_anomaly ? 'High' : 'Low'
                            }
                          },
                          sensor_stats: sensorPredictions.sensor_stats
                        });
                      } else {
                        const sensorData = generateSampleSensorData();
                        const predictions = await api.getCompletePrediction(sensorData, 'MACHINE-001');
                        setSystemData(predictions);
                      }
                    } catch (error) {
                      console.error('Refresh failed:', error);
                    }
                  }
                }}
              />
            </section>

            {/* Explainability Panel */}
            <ExplainabilityPanel 
              connectionStatus={connectionStatus}
              systemData={systemData}
            />

            {/* Alerts Section */}
            <section id="alerts" className="space-y-6">
              <div className="text-center space-y-2">
                <h2 className="text-3xl font-bold">Maintenance Alerts</h2>
                <p className="text-muted-foreground">
                  {useSensorData 
                    ? `Real-time notifications based on ${systemData?.sensor_stats?.active_sensors || 0} active sensors` 
                    : "Critical notifications and system warnings"}
                </p>
              </div>

              <div className="space-y-4">
                {/* Dynamic Alerts based on actual sensor/system data */}
                {systemData?.sensor_stats?.critical_sensors > 0 && (
                  <AlertCard
                    level="error"
                    title="Critical: Immediate Action Required"
                    message={`${systemData.sensor_stats.critical_sensors} critical sensor${systemData.sensor_stats.critical_sensors > 1 ? 's' : ''} detected! System health at ${systemData.sensor_stats.health_score}%. Multiple sensors are showing critical readings indicating immediate maintenance required.`}
                    timestamp="Just now"
                    machineId="SENSOR-NETWORK"
                    priority="critical"
                    onAcknowledge={() => console.log('Critical alert acknowledged')}
                    onDismiss={() => console.log('Critical alert dismissed')}
                    onViewDetails={() => window.location.href = '/sensors'}
                  />
                )}
                
                {systemData?.predictions?.rul?.value < 24 && (
                  <AlertCard
                    level="error"
                    title="Low RUL Warning: Maintenance Required"
                    message={`Remaining Useful Life is critically low at ${Math.round(systemData.predictions.rul.value)} hours. Immediate maintenance scheduling recommended to prevent equipment failure.`}
                    timestamp="2 minutes ago"
                    machineId="PRODUCTION-LINE"
                    priority="critical"
                    onAcknowledge={() => console.log('RUL alert acknowledged')}
                    onViewDetails={() => console.log('View RUL details')}
                  />
                )}
                
                {systemData?.predictions?.anomaly?.is_anomaly && (
                  <AlertCard
                    level="warning"
                    title="Anomaly Detected"
                    message={`Abnormal pattern detected with score ${Math.abs(systemData.predictions.anomaly.score || systemData.predictions.anomaly.anomaly_score).toFixed(3)}. System behavior deviating from normal operational parameters.`}
                    timestamp="5 minutes ago"
                    machineId="ANOMALY-DETECTION"
                    priority="high"
                    onAcknowledge={() => console.log('Anomaly alert acknowledged')}
                    onViewDetails={() => console.log('View anomaly details')}
                  />
                )}
                
                {systemData?.sensor_stats?.warning_sensors > 2 && (
                  <AlertCard
                    level="warning"
                    title="Maintenance Recommended"
                    message={`${systemData.sensor_stats.warning_sensors} sensors showing warning status. Preventive maintenance recommended within 48 hours to avoid degradation.`}
                    timestamp="1 hour ago"
                    machineId="SENSOR-NETWORK"
                    priority="high"
                    onAcknowledge={() => console.log('Warning alert acknowledged')}
                    onViewDetails={() => window.location.href = '/sensors'}
                  />
                )}
                
                {systemData?.predictions?.rul?.value >= 24 && systemData?.predictions?.rul?.value < 72 && (
                  <AlertCard
                    level="warning"
                    title="Scheduled Maintenance Approaching"
                    message={`RUL prediction indicates maintenance needed within ${Math.round(systemData.predictions.rul.value)} hours. Plan maintenance window to minimize downtime.`}
                    timestamp="2 hours ago"
                    machineId="MAINTENANCE-SCHEDULER"
                    priority="medium"
                    onAcknowledge={() => console.log('Scheduled maintenance acknowledged')}
                    onViewDetails={() => console.log('View maintenance schedule')}
                  />
                )}
                
                {systemData?.sensor_stats?.critical_sensors === 0 && systemData?.sensor_stats?.warning_sensors <= 2 && (
                  <AlertCard
                    level="success"
                    title="All Systems Normal"
                    message={`All sensors operating within normal parameters. System health at ${systemData?.sensor_stats?.health_score || 95}%. ${systemData?.sensor_stats?.active_sensors || 0} sensors active and monitoring.`}
                    timestamp="Just now"
                    machineId="HEALTH-MONITOR"
                    priority="low"
                  />
                )}
                
                {connectionStatus === 'connected' && useSensorData && (
                  <AlertCard
                    level="info"
                    title="Real-Time Sensor Network Active"
                    message={`Connected to live sensor network. ${systemData?.sensor_stats?.active_sensors || 0} active sensors providing real-time data across production lines.`}
                    timestamp="5 minutes ago"
                    priority="medium"
                    onViewDetails={() => window.location.href = '/sensors'}
                  />
                )}
                
                {/* Fallback static alerts if no real data */}
                {(!systemData || !systemData.success) && (
                  <>
                    <AlertCard
                      level="info"
                      title="Demo Mode Active"
                      message="System is running in demonstration mode. Connect to backend to see real sensor data and predictions."
                      timestamp="Now"
                      priority="medium"
                    />
                    <AlertCard
                      level="success"
                      title="System Ready"
                      message="Predictive maintenance system initialized and ready for sensor connection."
                      timestamp="10 minutes ago"
                      priority="low"
                    />
                  </>
                )}
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <aside className="lg:col-span-1">
            <DashboardSidebar sensorData={systemData} />
          </aside>
        </div>
      </div>

      {/* Footer */}
      <footer id="about" className="glass-card mt-16 py-16 border-t border-border">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8 mb-12">
            {/* Brand Section */}
            <div className="md:col-span-2 space-y-4">
              <div className="flex items-center gap-2">
                <Activity className="h-6 w-6 text-primary" />
                <span className="text-xl font-bold bg-gradient-to-r from-foreground to-primary bg-clip-text text-transparent">
                  PredictMaint AI
                </span>
              </div>
              <p className="text-muted-foreground max-w-md">
                Advanced predictive maintenance platform powered by explainable AI. 
                Monitor, predict, and prevent equipment failures with transparent, data-driven insights.
              </p>
              <div className="flex gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">99.9%</div>
                  <div className="text-xs text-muted-foreground">Accuracy</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">24/7</div>
                  <div className="text-xs text-muted-foreground">Monitoring</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">&lt; 1ms</div>
                  <div className="text-xs text-muted-foreground">Response</div>
                </div>
              </div>
            </div>

            {/* Features */}
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">Features</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="hover:text-primary cursor-pointer transition-colors">Real-time Monitoring</li>
                <li className="hover:text-primary cursor-pointer transition-colors">Anomaly Detection</li>
                <li className="hover:text-primary cursor-pointer transition-colors">SHAP Explanations</li>
                <li className="hover:text-primary cursor-pointer transition-colors">LIME Analysis</li>
                <li className="hover:text-primary cursor-pointer transition-colors">Risk Assessment</li>
              </ul>
            </div>

            {/* Resources */}
            <div className="space-y-4">
              <h4 className="font-semibold text-foreground">Resources</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="hover:text-primary cursor-pointer transition-colors">Documentation</li>
                <li className="hover:text-primary cursor-pointer transition-colors">API Reference</li>
                <li className="hover:text-primary cursor-pointer transition-colors">Support Center</li>
                <li className="hover:text-primary cursor-pointer transition-colors">System Status</li>
                <li className="hover:text-primary cursor-pointer transition-colors">Contact Us</li>
              </ul>
            </div>
          </div>

          {/* Bottom Section */}
          <div className="pt-8 border-t border-border">
            <div className="flex flex-col md:flex-row justify-between items-center gap-4">
              <div className="flex items-center gap-4 text-sm text-muted-foreground">
                <span>© 2025 PredictMaint AI Dashboard</span>
                <span className="hidden md:inline">•</span>
                <span className="hover:text-primary cursor-pointer transition-colors">Privacy Policy</span>
                <span>•</span>
                <span className="hover:text-primary cursor-pointer transition-colors">Terms of Service</span>
              </div>
              
              <div className="flex items-center gap-4 text-sm">
                <Badge variant="outline" className="gap-1">
                  <div className="w-2 h-2 bg-success rounded-full animate-pulse" />
                  System Operational
                </Badge>
                <span className="text-muted-foreground">v2.1.0</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
