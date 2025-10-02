"""
Explainability module for AI models using SHAP and LIME
Provides interpretable explanations for model predictions
"""

import numpy as np
import pandas as pd
import shap
import lime
import lime.lime_tabular
from typing import Dict, List, Any, Tuple, Optional
import logging
import json

logger = logging.getLogger(__name__)

class ModelExplainer:
    """Provides SHAP and LIME explanations for model predictions"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.shap_explainers = {}
        self.lime_explainers = {}
        self.feature_names = self._get_feature_names()
        self._initialize_explainers()
    
    def _get_feature_names(self) -> List[str]:
        """Get standardized feature names"""
        features = []
        
        # Operational settings
        for i in range(1, 4):
            features.append(f'setting_{i}')
        
        # Sensor measurements
        for i in range(1, 22):
            features.append(f'sensor_{i}')
        
        return features
    
    def _initialize_explainers(self):
        """Initialize SHAP and LIME explainers for all models"""
        try:
            # Generate background data for SHAP
            from .pretrained_models import generate_synthetic_turbofan_data
            background_data, _, _ = generate_synthetic_turbofan_data(1000)
            
            # Initialize SHAP explainers
            self._init_shap_explainers(background_data)
            
            # Initialize LIME explainers
            self._init_lime_explainers(background_data)
            
            logger.info("Explainers initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize explainers: {str(e)}")
    
    def _init_shap_explainers(self, background_data: pd.DataFrame):
        """Initialize SHAP explainers"""
        try:
            # Scale background data for each model
            if 'rul_scaler' in self.model_manager.scalers:
                rul_background = self.model_manager.scalers['rul_scaler'].transform(background_data)
                self.shap_explainers['rul'] = shap.Explainer(
                    self.model_manager.models['rul_predictor'],
                    rul_background[:100]  # Use subset for efficiency
                )
            
            if 'failure_scaler' in self.model_manager.scalers:
                failure_background = self.model_manager.scalers['failure_scaler'].transform(background_data)
                self.shap_explainers['failure'] = shap.Explainer(
                    self.model_manager.models['failure_classifier'],
                    failure_background[:100]
                )
                
        except Exception as e:
            logger.warning(f"SHAP explainer initialization failed: {str(e)}")
    
    def _init_lime_explainers(self, background_data: pd.DataFrame):
        """Initialize LIME explainers"""
        try:
            # LIME explainer for tabular data
            self.lime_explainers['tabular'] = lime.lime_tabular.LimeTabularExplainer(
                background_data.values,
                feature_names=self.feature_names,
                class_names=['Low Risk', 'Medium Risk', 'High Risk'],
                mode='classification',
                discretize_continuous=True
            )
            
        except Exception as e:
            logger.warning(f"LIME explainer initialization failed: {str(e)}")
    
    def get_shap_explanation(self, 
                           model_type: str, 
                           input_data: np.ndarray,
                           max_display: int = 10) -> Dict[str, Any]:
        """
        Get SHAP explanation for a prediction
        
        Args:
            model_type: 'rul' or 'failure'
            input_data: Input features [24 features]
            max_display: Maximum number of features to display
            
        Returns:
            Dictionary with SHAP values and explanations
        """
        try:
            if model_type not in self.shap_explainers:
                raise ValueError(f"SHAP explainer not available for {model_type}")
            
            # Scale input data
            scaler_key = f'{model_type}_scaler'
            if scaler_key in self.model_manager.scalers:
                scaled_data = self.model_manager.scalers[scaler_key].transform(
                    input_data.reshape(1, -1)
                )
            else:
                scaled_data = input_data.reshape(1, -1)
            
            # Get SHAP values
            explainer = self.shap_explainers[model_type]
            shap_values = explainer(scaled_data)
            
            # Process SHAP values
            if hasattr(shap_values, 'values'):
                values = shap_values.values[0]
                base_value = shap_values.base_values[0] if hasattr(shap_values, 'base_values') else 0
            else:
                values = shap_values[0]
                base_value = 0
            
            # Handle multi-class output
            if len(values.shape) > 1:
                values = values[:, 1]  # Use positive class for binary classification
            
            # Create feature importance ranking
            feature_importance = []
            for i, (feature, value) in enumerate(zip(self.feature_names, values)):
                feature_importance.append({
                    'feature': feature,
                    'shap_value': float(value),
                    'abs_importance': float(abs(value)),
                    'impact': 'positive' if value > 0 else 'negative'
                })
            
            # Sort by absolute importance
            feature_importance.sort(key=lambda x: x['abs_importance'], reverse=True)
            
            return {
                'model_type': model_type,
                'base_value': float(base_value),
                'feature_importance': feature_importance[:max_display],
                'total_features': len(self.feature_names),
                'explanation_type': 'SHAP',
                'summary': self._generate_shap_summary(feature_importance[:5])
            }
            
        except Exception as e:
            logger.error(f"SHAP explanation failed: {str(e)}")
            return {
                'error': str(e),
                'model_type': model_type,
                'explanation_type': 'SHAP'
            }
    
    def get_lime_explanation(self, 
                           input_data: np.ndarray,
                           model_type: str = 'failure',
                           num_features: int = 10) -> Dict[str, Any]:
        """
        Get LIME explanation for a prediction
        
        Args:
            input_data: Input features [24 features]
            model_type: Type of model to explain
            num_features: Number of features to include in explanation
            
        Returns:
            Dictionary with LIME explanations
        """
        try:
            if 'tabular' not in self.lime_explainers:
                raise ValueError("LIME explainer not available")
            
            # Define prediction function for LIME
            def predict_fn(X):
                if model_type == 'rul':
                    predictions = []
                    for x in X:
                        pred, _ = self.model_manager.predict_rul(x)
                        # Convert to probability-like format for LIME
                        prob = 1.0 / (1.0 + np.exp(-pred / 100))  # Sigmoid transformation
                        predictions.append([1-prob, prob])
                    return np.array(predictions)
                else:  # failure classification
                    predictions = []
                    for x in X:
                        risk_class, metadata = self.model_manager.predict_failure_risk(x)
                        probs = list(metadata['probabilities'].values())
                        predictions.append(probs)
                    return np.array(predictions)
            
            # Get LIME explanation
            explainer = self.lime_explainers['tabular']
            explanation = explainer.explain_instance(
                input_data,
                predict_fn,
                num_features=num_features
            )
            
            # Process LIME explanation
            lime_features = []
            for feature, importance in explanation.as_list():
                lime_features.append({
                    'feature': feature,
                    'importance': float(importance),
                    'abs_importance': float(abs(importance)),
                    'impact': 'positive' if importance > 0 else 'negative'
                })
            
            # Sort by absolute importance
            lime_features.sort(key=lambda x: x['abs_importance'], reverse=True)
            
            return {
                'model_type': model_type,
                'feature_importance': lime_features,
                'local_prediction': explanation.predict_proba[1] if len(explanation.predict_proba) > 1 else explanation.predict_proba[0],
                'explanation_type': 'LIME',
                'summary': self._generate_lime_summary(lime_features[:3])
            }
            
        except Exception as e:
            logger.error(f"LIME explanation failed: {str(e)}")
            return {
                'error': str(e),
                'model_type': model_type,
                'explanation_type': 'LIME'
            }
    
    def get_feature_impact_analysis(self, input_data: np.ndarray) -> Dict[str, Any]:
        """
        Comprehensive feature impact analysis combining SHAP and LIME
        
        Args:
            input_data: Input features [24 features]
            
        Returns:
            Combined analysis results
        """
        try:
            # Get SHAP explanations for both models
            shap_rul = self.get_shap_explanation('rul', input_data)
            shap_failure = self.get_shap_explanation('failure', input_data)
            
            # Get LIME explanation
            lime_explanation = self.get_lime_explanation(input_data, 'failure')
            
            # Combine and analyze
            combined_analysis = {
                'shap_rul': shap_rul,
                'shap_failure': shap_failure,
                'lime_local': lime_explanation,
                'consensus_features': self._find_consensus_features(shap_rul, shap_failure, lime_explanation),
                'analysis_timestamp': pd.Timestamp.now().isoformat()
            }
            
            return combined_analysis
            
        except Exception as e:
            logger.error(f"Feature impact analysis failed: {str(e)}")
            return {'error': str(e)}
    
    def _generate_shap_summary(self, top_features: List[Dict]) -> str:
        """Generate human-readable SHAP summary"""
        if not top_features:
            return "No significant features identified."
        
        top_feature = top_features[0]
        impact_word = "increases" if top_feature['impact'] == 'positive' else "decreases"
        
        summary = f"The most influential factor is {top_feature['feature']}, which {impact_word} the prediction. "
        
        if len(top_features) > 1:
            other_features = [f['feature'] for f in top_features[1:3]]
            summary += f"Other important factors include {', '.join(other_features)}."
        
        return summary
    
    def _generate_lime_summary(self, top_features: List[Dict]) -> str:
        """Generate human-readable LIME summary"""
        if not top_features:
            return "No significant local features identified."
        
        top_feature = top_features[0]
        impact_word = "increases" if top_feature['impact'] == 'positive' else "decreases"
        
        return f"For this specific instance, {top_feature['feature']} {impact_word} the prediction the most."
    
    def _find_consensus_features(self, shap_rul: Dict, shap_failure: Dict, lime_exp: Dict) -> List[str]:
        """Find features that are important across different explanation methods"""
        consensus = []
        
        try:
            # Get top features from each method
            shap_rul_features = {f['feature'] for f in shap_rul.get('feature_importance', [])[:5]}
            shap_failure_features = {f['feature'] for f in shap_failure.get('feature_importance', [])[:5]}
            lime_features = {f['feature'].split(' ')[0] for f in lime_exp.get('feature_importance', [])[:5]}  # LIME might have ranges
            
            # Find intersection
            all_features = [shap_rul_features, shap_failure_features, lime_features]
            consensus = list(set.intersection(*all_features))
            
        except Exception as e:
            logger.warning(f"Consensus analysis failed: {str(e)}")
        
        return consensus
