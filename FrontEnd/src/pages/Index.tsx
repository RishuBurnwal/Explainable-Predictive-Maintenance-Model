import Navigation from "@/components/Navigation";
import Hero from "@/components/Hero";
import StatusCard from "@/components/StatusCard";
import DataVisualization from "@/components/DataVisualization";
import ExplainabilityPanel from "@/components/ExplainabilityPanel";
import AlertCard from "@/components/AlertCard";
import DashboardSidebar from "@/components/DashboardSidebar";
import { Activity, Gauge, AlertTriangle, CheckCircle } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { useState, useEffect } from "react";
import { usePredictiveMaintenanceAPI, generateSampleSensorData } from "@/lib/api";

const Index = () => {
  const { api, testConnection, getCompletePrediction } = usePredictiveMaintenanceAPI();
  const [systemData, setSystemData] = useState<any>(null);
  const [connectionStatus, setConnectionStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const initializeSystem = async () => {
      setIsLoading(true);
      
      // Test connection
      const connection = await testConnection();
      setConnectionStatus(connection.connected ? 'connected' : 'disconnected');
      
      if (connection.connected) {
        // Get initial predictions
        const sensorData = generateSampleSensorData();
        const predictions = await getCompletePrediction(sensorData, 'MACHINE-001');
        setSystemData(predictions);
      }
      
      setIsLoading(false);
    };

    initializeSystem();
    
    // Set up periodic updates
    const interval = setInterval(async () => {
      if (connectionStatus === 'connected') {
        const sensorData = generateSampleSensorData();
        const predictions = await getCompletePrediction(sensorData, 'MACHINE-001');
        setSystemData(predictions);
      }
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const getStatusCardData = () => {
    if (!systemData?.success) {
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
          value: connectionStatus === 'checking' ? "Loading..." : "82 hrs", 
          status: "success" as const, 
          description: connectionStatus === 'checking' ? "Initializing model..." : "Simulated prediction data", 
          trend: "down" as const, 
          percentage: "15%" 
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
    const rul = predictions.rul;
    const risk = predictions.risk;
    const anomaly = predictions.anomaly;

    return {
      engineStatus: {
        value: connectionStatus === 'connected' ? "Running" : "Offline",
        status: connectionStatus === 'connected' ? "success" as const : "error" as const,
        description: connectionStatus === 'connected' ? "All systems operational" : "Connection lost",
        trend: "stable" as const,
        percentage: "0%"
      },
      rulPrediction: {
        value: `${Math.round(rul.rul_prediction)} hrs`,
        status: rul.risk_level === 'High' ? "error" as const : rul.risk_level === 'Medium' ? "warning" as const : "success" as const,
        description: `Confidence: ${Math.round(rul.confidence * 100)}%`,
        trend: rul.risk_level === 'High' ? "down" as const : "stable" as const,
        percentage: `${Math.round((1 - rul.confidence) * 100)}%`
      },
      riskLevel: {
        value: risk.risk_class,
        status: risk.risk_class === 'High' ? "error" as const : risk.risk_class === 'Medium' ? "warning" as const : "success" as const,
        description: `Risk Score: ${risk.risk_score.toFixed(2)}`,
        trend: risk.risk_class === 'High' ? "up" as const : "stable" as const,
        percentage: `${Math.round(risk.risk_probabilities[risk.risk_class] * 100)}%`
      },
      anomalyStatus: {
        value: anomaly.is_anomaly ? `${anomaly.severity} Risk` : "Normal",
        status: anomaly.is_anomaly ? (anomaly.severity === 'High' ? "error" as const : "warning" as const) : "success" as const,
        description: anomaly.is_anomaly ? `Score: ${anomaly.anomaly_score.toFixed(3)}` : "No anomalies detected",
        trend: anomaly.is_anomaly ? "up" as const : "stable" as const,
        percentage: `${Math.round(anomaly.anomaly_score * 100)}%`
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
        <div className="grid lg:grid-cols-4 gap-8">
          <div className="lg:col-span-3 space-y-16">
            {/* Status Cards Section */}
            <section id="dashboard" className="space-y-6 animate-fade-in">
              <div className="text-center space-y-2">
                <h2 className="text-3xl font-bold">Real-Time System Status</h2>
                <p className="text-muted-foreground">Live monitoring of critical machine health indicators</p>
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
                    Connected to live backend
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
                    const sensorData = generateSampleSensorData();
                    const predictions = await getCompletePrediction(sensorData, 'MACHINE-001');
                    setSystemData(predictions);
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
                <p className="text-muted-foreground">Critical notifications and system warnings</p>
              </div>

              <div className="space-y-4">
                <AlertCard
                  level="error"
                  title="Critical: Immediate Action Required"
                  message="Temperature exceeds safety threshold (95°C). Automatic shutdown has been initiated to prevent equipment damage. Engineering team has been notified and is responding to the incident."
                  timestamp="2 minutes ago"
                  machineId="MACHINE-001"
                  priority="critical"
                  onAcknowledge={() => console.log('Critical alert acknowledged')}
                  onDismiss={() => console.log('Critical alert dismissed')}
                  onViewDetails={() => console.log('View critical alert details')}
                />
                <AlertCard
                  level="warning"
                  title="Maintenance Recommended"
                  message="RUL prediction indicates maintenance needed within 48 hours. Vibration levels have increased by 15% over the past week, suggesting bearing wear."
                  timestamp="1 hour ago"
                  machineId="MACHINE-002"
                  priority="high"
                  onAcknowledge={() => console.log('Warning alert acknowledged')}
                  onViewDetails={() => console.log('View warning alert details')}
                />
                <AlertCard
                  level="success"
                  title="Maintenance Completed Successfully"
                  message="Scheduled maintenance successfully completed. All systems are now operating within normal parameters. Next maintenance due in 30 days."
                  timestamp="3 hours ago"
                  machineId="MACHINE-003"
                  priority="low"
                />
                <AlertCard
                  level="info"
                  title="System Performance Update"
                  message="Weekly performance report: Overall equipment effectiveness increased by 3.2%. Anomaly detection accuracy improved to 97.8%."
                  timestamp="6 hours ago"
                  priority="medium"
                  onViewDetails={() => console.log('View performance report')}
                />
              </div>
            </section>
          </div>

          {/* Sidebar */}
          <aside className="lg:col-span-1">
            <DashboardSidebar />
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
