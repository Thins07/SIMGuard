export interface FileUploadResponse {
  status: string;
  message: string;
  filename: string;
  records_count: number;
  columns: string[];
  date_range: {
    start: string;
    end: string;
  };
}

export interface SuspiciousActivity {
  timestamp: string;
  user_id: string;
  sim_id: string;
  risk_level: string;
  flag_reason: string;
}

export interface RiskDistribution {
  High: number;
  Medium: number;
  Low: number;
}

export interface AnalysisSummary {
  users_analyzed: number;
  high_risk_users: number;
  medium_risk_users: number;
  clean_users: number;
}

export interface AnalysisResult {
  status: string;
  analysis_timestamp: string;
  summary: {
    total_records: number;
    suspicious_count: number;
    clean_count: number;
    users_analyzed: number;
    high_risk_users: number;
    medium_risk_users: number;
    clean_users: number;
  };
  risk_distribution: RiskDistribution;
  suspicious_activities: SuspiciousActivity[];
  total_suspicious_activities: number;
}

// --- NEW TYPES FOR ML DASHBOARD ---

export interface PredictionRequest {
  distance_change: number;
  time_since_sim_change: number;
  num_failed_logins_last_24h: number;
  num_calls_last_24h: number;
  num_sms_last_24h: number;
  data_usage_last_24h: number; // ADDED: Core feature for Thinker Model
  data_usage_change_percent: number;
  change_in_cell_tower_id: number;
  is_roaming: boolean;
  sim_change_flag: boolean;
  device_change_flag: boolean;
  current_city: string;
  previous_city: string;
}

export interface PredictionResponse {
  status: string;
  prediction: number; // 0 or 1
  confidence: number; // 0.0 to 1.0
  risk_level: 'HIGH' | 'MEDIUM' | 'LOW';
  message: string;
}

// --- NEW TYPES FOR TRAINING DASHBOARD ---

export interface TrainRequest {
  model_type: 'xgboost' | 'random_forest' | 'logistic';
  test_size: number;
}

export interface TrainResponse {
  status: string;
  model_type: string;
  metrics: {
    accuracy: number;
    precision: number;
    recall: number;
    f1_score: number;
  };
  confusion_matrix: number[][];
  features: string[];
}

export type ViewState = 'home' | 'upload' | 'dashboard' | 'ml-manual' | 'sl-training';