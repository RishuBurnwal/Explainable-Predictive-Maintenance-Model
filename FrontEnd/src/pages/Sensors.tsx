import { useState, useEffect } from "react";
import Navigation from "@/components/Navigation";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Slider } from "@/components/ui/slider";
import { 
  Activity, 
  Thermometer, 
  Radio, 
  Gauge, 
  Zap, 
  Wind,
  MapPin,
  RefreshCw,
  AlertCircle,
  CheckCircle2,
  XCircle,
  TrendingUp
} from "lucide-react";
import PredictiveMaintenanceAPI, { SensorData, SensorStatistics } from "@/lib/api";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

// Sensor type icon mapping
const sensorIcons: Record<string, any> = {
  temperature: Thermometer,
  vibration: Radio,
  pressure: Gauge,
  rpm: Activity,
  flow_rate: Wind,
  current: Zap,
  voltage: Zap,
  torque: Activity,
};

// Status color mapping
const statusColors = {
  normal: "bg-green-500",
  warning: "bg-yellow-500",
  critical: "bg-red-500",
  offline: "bg-gray-500",
};

const statusBadgeVariants = {
  normal: "default" as const,
  warning: "secondary" as const,
  critical: "destructive" as const,
  offline: "outline" as const,
};

interface SensorCardProps {
  sensor: SensorData;
  onToggle: (sensorId: string, isActive: boolean) => void;
  onAgeChange: (sensorId: string, age: number) => void;
  isUpdating: boolean;
}

const SensorCard = ({ sensor, onToggle, onAgeChange, isUpdating }: SensorCardProps) => {
  const Icon = sensorIcons[sensor.type] || Activity;
  const [ageValue, setAgeValue] = useState(sensor.age_percentage || 0);
  
  return (
    <Card className="glass-card card-3d group hover:shadow-xl transition-all duration-300">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className={`p-3 rounded-lg ${
              sensor.is_active ? 'bg-primary/10' : 'bg-muted'
            } transition-colors`}>
              <Icon className={`w-5 h-5 ${
                sensor.is_active ? 'text-primary' : 'text-muted-foreground'
              }`} />
            </div>
            <div>
              <CardTitle className="text-base">{sensor.name}</CardTitle>
              <CardDescription className="text-xs mt-1">
                ID: {sensor.sensor_id}
              </CardDescription>
            </div>
          </div>
          <Badge variant={statusBadgeVariants[sensor.status]}>
            {sensor.status.toUpperCase()}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Location */}
        <div className="flex items-start gap-2 text-sm">
          <MapPin className="w-4 h-4 text-muted-foreground mt-0.5 flex-shrink-0" />
          <div>
            <p className="font-medium text-xs text-muted-foreground mb-1">Location</p>
            <p className="text-sm leading-tight">{sensor.location}</p>
          </div>
        </div>
        
        {/* Description */}
        <div className="text-sm">
          <p className="font-medium text-xs text-muted-foreground mb-1">Description</p>
          <p className="text-xs leading-relaxed text-muted-foreground">
            {sensor.description}
          </p>
        </div>
        
        {/* Current Reading */}
        {sensor.is_active && (
          <div className="p-3 bg-muted/50 rounded-lg">
            <div className="flex items-center justify-between">
              <span className="text-xs text-muted-foreground">Current Reading</span>
              <div className="flex items-center gap-2">
                <span className="text-2xl font-bold">
                  {sensor.current_value.toFixed(1)}
                </span>
                <span className="text-xs text-muted-foreground">
                  {sensor.type === 'temperature' ? '°C' : 
                   sensor.type === 'pressure' ? 'PSI' :
                   sensor.type === 'rpm' ? 'RPM' :
                   sensor.type === 'vibration' ? 'mm/s' :
                   sensor.type === 'current' ? 'A' :
                   sensor.type === 'voltage' ? 'V' :
                   sensor.type === 'torque' ? 'Nm' :
                   sensor.type === 'flow_rate' ? 'L/min' : ''}
                </span>
              </div>
            </div>
            
            {/* Status Indicator */}
            <div className="mt-2 flex items-center gap-2">
              <div className={`w-2 h-2 rounded-full ${statusColors[sensor.status]} ${
                sensor.status !== 'offline' ? 'animate-pulse' : ''
              }`} />
              <span className="text-xs">
                {sensor.status === 'normal' ? 'Operating Normally' :
                 sensor.status === 'warning' ? 'Warning Threshold' :
                 sensor.status === 'critical' ? 'Critical Alert' : 'Offline'}
              </span>
            </div>
          </div>
        )}
        
        {/* Age/Degradation Slider */}
        <div className="space-y-2 pt-2 border-t">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-muted-foreground">Age/Degradation</span>
            <span className="text-xs font-bold text-primary">{ageValue}%</span>
          </div>
          <Slider
            value={[ageValue]}
            onValueChange={(value) => setAgeValue(value[0])}
            onValueCommit={(value) => onAgeChange(sensor.sensor_id, value[0])}
            min={0}
            max={100}
            step={1}
            className="w-full"
            disabled={isUpdating || !sensor.is_active}
          />
          <p className="text-xs text-muted-foreground">
            {ageValue === 0 ? 'Brand New' : 
             ageValue < 30 ? 'Good Condition' :
             ageValue < 60 ? 'Moderate Wear' :
             ageValue < 80 ? 'High Wear' : 'Critical Degradation'}
          </p>
        </div>
        
        {/* Toggle Control */}
        <div className="flex items-center justify-between pt-2 border-t">
          <span className="text-sm font-medium">
            {sensor.is_active ? 'Active' : 'Inactive'}
          </span>
          <Switch
            checked={sensor.is_active}
            onCheckedChange={(checked) => onToggle(sensor.sensor_id, checked)}
            disabled={isUpdating}
          />
        </div>
        
        {/* Last Updated */}
        <div className="text-xs text-muted-foreground text-right">
          Updated: {new Date(sensor.last_updated).toLocaleTimeString()}
        </div>
      </CardContent>
    </Card>
  );
};

const Sensors = () => {
  const [sensors, setSensors] = useState<SensorData[]>([]);
  const [statistics, setStatistics] = useState<SensorStatistics | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [updatingSensors, setUpdatingSensors] = useState<Set<string>>(new Set());
  const [error, setError] = useState<string | null>(null);
  const [filterStatus, setFilterStatus] = useState<string>('all');
  const [filterLocation, setFilterLocation] = useState<string>('all');
  
  const api = new PredictiveMaintenanceAPI();

  const loadSensors = async () => {
    try {
      setError(null);
      const [sensorsData, stats] = await Promise.all([
        api.getAllSensors(false),
        api.getSensorStatistics(),
      ]);
      setSensors(sensorsData);
      setStatistics(stats);
    } catch (err) {
      setError('Failed to load sensors. Please ensure the backend is running.');
      console.error('Error loading sensors:', err);
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  };

  useEffect(() => {
    loadSensors();
    
    // Auto-refresh every 5 seconds
    const interval = setInterval(() => {
      loadSensors();
    }, 5000);
    
    return () => clearInterval(interval);
  }, []);

  const handleToggleSensor = async (sensorId: string, isActive: boolean) => {
    setUpdatingSensors(prev => new Set(prev).add(sensorId));
    
    try {
      await api.toggleSensor(sensorId, isActive);
      await loadSensors(); // Reload to get updated data
    } catch (err) {
      console.error('Error toggling sensor:', err);
      setError('Failed to toggle sensor');
    } finally {
      setUpdatingSensors(prev => {
        const next = new Set(prev);
        next.delete(sensorId);
        return next;
      });
    }
  };

  const handleAgeChange = async (sensorId: string, age: number) => {
    setUpdatingSensors(prev => new Set(prev).add(sensorId));
    
    try {
      await api.setSensorAge(sensorId, age);
      await loadSensors(); // Reload to get updated data
    } catch (err) {
      console.error('Error setting sensor age:', err);
      setError('Failed to set sensor age');
    } finally {
      setUpdatingSensors(prev => {
        const next = new Set(prev);
        next.delete(sensorId);
        return next;
      });
    }
  };

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await loadSensors();
  };

  const filteredSensors = sensors.filter(sensor => {
    if (filterStatus === 'all') return true;
    if (filterStatus === 'active') return sensor.is_active;
    if (filterStatus === 'inactive') return !sensor.is_active;
    return sensor.status === filterStatus;
  });

  // Group sensors by production line/location
  const groupedSensors = filteredSensors.reduce((groups, sensor) => {
    // Extract production line from location
    const locationMatch = sensor.location.match(/Production Line [A-D]|Quality Control|Central Cooling System/);
    const group = locationMatch ? locationMatch[0] : 'Other';
    
    if (filterLocation === 'all' || group === filterLocation) {
      if (!groups[group]) {
        groups[group] = [];
      }
      groups[group].push(sensor);
    }
    return groups;
  }, {} as Record<string, SensorData[]>);

  // Get unique locations for filter
  const uniqueLocations = Array.from(new Set(sensors.map(s => {
    const locationMatch = s.location.match(/Production Line [A-D]|Quality Control|Central Cooling System/);
    return locationMatch ? locationMatch[0] : 'Other';
  }))).sort();

  if (isLoading) {
    return (
      <div className="min-h-screen">
        <Navigation />
        <div className="container mx-auto px-4 py-16">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
              <p className="text-muted-foreground">Loading sensor network...</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <Navigation />
      
      <div className="container mx-auto px-4 py-16">
        {/* Header */}
        <div className="text-center space-y-4 mb-12">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
            Factory Sensor Network
          </h1>
          <p className="text-muted-foreground text-lg">
            Real-time monitoring and control of industrial IoT sensors
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Error</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Statistics Dashboard */}
        {statistics && (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
            <Card className="glass-card">
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-3xl font-bold text-primary">{statistics.total_sensors}</p>
                  <p className="text-xs text-muted-foreground mt-1">Total Sensors</p>
                </div>
              </CardContent>
            </Card>
            
            <Card className="glass-card">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-1">
                    <CheckCircle2 className="w-4 h-4 text-green-500" />
                    <p className="text-3xl font-bold text-green-500">{statistics.active_sensors}</p>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">Active</p>
                </div>
              </CardContent>
            </Card>
            
            <Card className="glass-card">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-1">
                    <XCircle className="w-4 h-4 text-gray-500" />
                    <p className="text-3xl font-bold text-gray-500">{statistics.inactive_sensors}</p>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">Inactive</p>
                </div>
              </CardContent>
            </Card>
            
            <Card className="glass-card">
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-3xl font-bold text-yellow-500">{statistics.warning_sensors}</p>
                  <p className="text-xs text-muted-foreground mt-1">Warnings</p>
                </div>
              </CardContent>
            </Card>
            
            <Card className="glass-card">
              <CardContent className="pt-6">
                <div className="text-center">
                  <p className="text-3xl font-bold text-red-500">{statistics.critical_sensors}</p>
                  <p className="text-xs text-muted-foreground mt-1">Critical</p>
                </div>
              </CardContent>
            </Card>
            
            <Card className="glass-card">
              <CardContent className="pt-6">
                <div className="text-center">
                  <div className="flex items-center justify-center gap-1">
                    <TrendingUp className="w-4 h-4 text-primary" />
                    <p className="text-3xl font-bold text-primary">{statistics.health_score}%</p>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1">Health Score</p>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Controls */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
          <div className="space-y-3 flex-1">
            {/* Status Filters */}
            <div className="flex flex-wrap gap-2">
              <span className="text-sm font-medium text-muted-foreground mr-2 self-center">Status:</span>
              <Button
                variant={filterStatus === 'all' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('all')}
              >
                All Sensors
              </Button>
              <Button
                variant={filterStatus === 'active' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('active')}
              >
                Active
              </Button>
              <Button
                variant={filterStatus === 'inactive' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('inactive')}
              >
                Inactive
              </Button>
              <Button
                variant={filterStatus === 'critical' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('critical')}
              >
                Critical
              </Button>
              <Button
                variant={filterStatus === 'warning' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilterStatus('warning')}
              >
                Warning
              </Button>
            </div>
            
            {/* Location Filters */}
            <div className="flex flex-wrap gap-2">
              <span className="text-sm font-medium text-muted-foreground mr-2 self-center">Location:</span>
              <Button
                variant={filterLocation === 'all' ? 'default' : 'outline'}
                size="sm"
                onClick={() => setFilterLocation('all')}
              >
                All Locations
              </Button>
              {uniqueLocations.map(location => (
                <Button
                  key={location}
                  variant={filterLocation === location ? 'default' : 'outline'}
                  size="sm"
                  onClick={() => setFilterLocation(location)}
                >
                  {location}
                </Button>
              ))}
            </div>
          </div>
          
          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="gap-2"
          >
            <RefreshCw className={`w-4 h-4 ${isRefreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>

        {/* Sensor Grid - Grouped by Location */}
        {Object.entries(groupedSensors).length === 0 ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">No sensors found matching the current filters</p>
          </div>
        ) : (
          <div className="space-y-8">
            {Object.entries(groupedSensors).sort(([a], [b]) => a.localeCompare(b)).map(([location, locationSensors]) => (
              <div key={location}>
                {/* Location Header */}
                <div className="flex items-center gap-3 mb-4">
                  <div className="flex items-center gap-2 bg-primary/10 px-4 py-2 rounded-lg">
                    <MapPin className="w-5 h-5 text-primary" />
                    <h2 className="text-xl font-semibold">{location}</h2>
                  </div>
                  <Badge variant="outline">
                    {locationSensors.length} sensor{locationSensors.length !== 1 ? 's' : ''}
                  </Badge>
                </div>
                
                {/* Sensors in this location */}
                <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {locationSensors.map((sensor) => (
                    <SensorCard
                      key={sensor.sensor_id}
                      sensor={sensor}
                      onToggle={handleToggleSensor}
                      onAgeChange={handleAgeChange}
                      isUpdating={updatingSensors.has(sensor.sensor_id)}
                    />
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}

        {filteredSensors.length === 0 && (
          <div className="text-center py-12">
            <AlertCircle className="w-16 h-16 text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">No sensors found matching the filter</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Sensors;
