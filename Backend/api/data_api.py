"""
Data API endpoints for managing sensor data and datasets
"""

from flask import Blueprint, request, jsonify, send_file
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging
import io
import os

from AI.pretrained_models import generate_synthetic_turbofan_data

data_bp = Blueprint('data', __name__)
logger = logging.getLogger(__name__)

@data_bp.route('/generate-sample', methods=['POST'])
def generate_sample_data():
    """
    Generate sample turbofan engine data
    
    Expected input:
    {
        "num_samples": 1000,
        "format": "json" or "csv",
        "include_targets": true
    }
    """
    try:
        data = request.get_json() if request.get_json() else {}
        
        num_samples = data.get('num_samples', 1000)
        format_type = data.get('format', 'json')
        include_targets = data.get('include_targets', True)
        
        # Validate parameters
        if num_samples > 10000:
            return jsonify({'error': 'Maximum 10,000 samples allowed'}), 400
        
        if format_type not in ['json', 'csv']:
            return jsonify({'error': 'Format must be "json" or "csv"'}), 400
        
        # Generate data
        features_df, rul_targets, failure_targets = generate_synthetic_turbofan_data(num_samples)
        
        if include_targets:
            features_df['rul'] = rul_targets
            features_df['failure_risk'] = failure_targets
        
        # Add metadata columns
        features_df['machine_id'] = [f'MACHINE-{str(i+1).zfill(3)}' for i in range(num_samples)]
        features_df['timestamp'] = pd.date_range(
            start=datetime.now() - timedelta(days=30),
            periods=num_samples,
            freq='H'
        )
        
        if format_type == 'json':
            response_data = {
                'data': features_df.to_dict('records'),
                'metadata': {
                    'num_samples': num_samples,
                    'features': list(features_df.columns),
                    'generated_at': datetime.utcnow().isoformat()
                },
                'status': 'success'
            }
            return jsonify(response_data)
        
        else:  # CSV format
            output = io.StringIO()
            features_df.to_csv(output, index=False)
            output.seek(0)
            
            return send_file(
                io.BytesIO(output.getvalue().encode()),
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'turbofan_data_{num_samples}_samples.csv'
            )
        
    except Exception as e:
        logger.error(f"Sample data generation failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@data_bp.route('/upload', methods=['POST'])
def upload_data():
    """
    Upload and validate sensor data
    
    Expected: CSV file with sensor data
    """
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.csv'):
            return jsonify({'error': 'Only CSV files are supported'}), 400
        
        # Read CSV data
        try:
            df = pd.read_csv(file)
        except Exception as e:
            return jsonify({'error': f'Failed to read CSV file: {str(e)}'}), 400
        
        # Validate data structure
        required_columns = []
        for i in range(1, 4):
            required_columns.append(f'setting_{i}')
        for i in range(1, 22):
            required_columns.append(f'sensor_{i}')
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({
                'error': f'Missing required columns: {missing_columns}',
                'required_columns': required_columns,
                'found_columns': list(df.columns)
            }), 400
        
        # Basic data validation
        numeric_columns = required_columns
        non_numeric = []
        
        for col in numeric_columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                non_numeric.append(col)
        
        if non_numeric:
            return jsonify({
                'error': f'Non-numeric data found in columns: {non_numeric}'
            }), 400
        
        # Check for missing values
        missing_data = df[numeric_columns].isnull().sum()
        missing_info = {col: int(count) for col, count in missing_data.items() if count > 0}
        
        # Data quality metrics
        quality_metrics = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': missing_info,
            'data_types': {col: str(df[col].dtype) for col in df.columns},
            'numeric_columns': len(numeric_columns),
            'valid_rows': len(df.dropna(subset=numeric_columns))
        }
        
        # Sample statistics
        statistics = {}
        for col in numeric_columns:
            statistics[col] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max()),
                'missing_count': int(df[col].isnull().sum())
            }
        
        response = {
            'upload_status': 'success',
            'file_info': {
                'filename': file.filename,
                'size_bytes': len(file.read()),
                'upload_timestamp': datetime.utcnow().isoformat()
            },
            'data_quality': quality_metrics,
            'statistics': statistics,
            'validation_passed': len(missing_info) == 0,
            'recommendations': []
        }
        
        # Add recommendations
        if missing_info:
            response['recommendations'].append('Consider handling missing values before analysis')
        
        if quality_metrics['valid_rows'] < quality_metrics['total_rows']:
            response['recommendations'].append('Some rows contain missing values and may be excluded from analysis')
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Data upload failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@data_bp.route('/preprocess', methods=['POST'])
def preprocess_data():
    """
    Preprocess sensor data for model input
    
    Expected input:
    {
        "data": [
            {
                "setting_1": 0.1, "setting_2": 0.2, "setting_3": 0.3,
                "sensor_1": 1.0, "sensor_2": 1.1, ..., "sensor_21": 2.1
            },
            ...
        ],
        "preprocessing_options": {
            "normalize": true,
            "handle_missing": "mean",
            "remove_outliers": false
        }
    }
    """
    try:
        request_data = request.get_json()
        
        if not request_data or 'data' not in request_data:
            return jsonify({'error': 'Missing data in request'}), 400
        
        data = request_data['data']
        options = request_data.get('preprocessing_options', {})
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Validate required columns
        required_columns = []
        for i in range(1, 4):
            required_columns.append(f'setting_{i}')
        for i in range(1, 22):
            required_columns.append(f'sensor_{i}')
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return jsonify({
                'error': f'Missing required columns: {missing_columns}'
            }), 400
        
        original_shape = df.shape
        preprocessing_steps = []
        
        # Handle missing values
        handle_missing = options.get('handle_missing', 'mean')
        if df[required_columns].isnull().any().any():
            if handle_missing == 'mean':
                df[required_columns] = df[required_columns].fillna(df[required_columns].mean())
                preprocessing_steps.append('Filled missing values with column means')
            elif handle_missing == 'median':
                df[required_columns] = df[required_columns].fillna(df[required_columns].median())
                preprocessing_steps.append('Filled missing values with column medians')
            elif handle_missing == 'drop':
                df = df.dropna(subset=required_columns)
                preprocessing_steps.append('Dropped rows with missing values')
        
        # Remove outliers
        if options.get('remove_outliers', False):
            # Use IQR method
            Q1 = df[required_columns].quantile(0.25)
            Q3 = df[required_columns].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define outliers
            outlier_condition = (
                (df[required_columns] < (Q1 - 1.5 * IQR)) | 
                (df[required_columns] > (Q3 + 1.5 * IQR))
            ).any(axis=1)
            
            outliers_removed = outlier_condition.sum()
            df = df[~outlier_condition]
            preprocessing_steps.append(f'Removed {outliers_removed} outlier rows')
        
        # Normalize data
        if options.get('normalize', True):
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            df[required_columns] = scaler.fit_transform(df[required_columns])
            preprocessing_steps.append('Applied standard normalization (z-score)')
        
        # Calculate statistics
        final_stats = {}
        for col in required_columns:
            final_stats[col] = {
                'mean': float(df[col].mean()),
                'std': float(df[col].std()),
                'min': float(df[col].min()),
                'max': float(df[col].max())
            }
        
        response = {
            'preprocessed_data': df.to_dict('records'),
            'preprocessing_summary': {
                'original_shape': original_shape,
                'final_shape': df.shape,
                'steps_applied': preprocessing_steps,
                'rows_removed': original_shape[0] - df.shape[0]
            },
            'statistics': final_stats,
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Data preprocessing failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@data_bp.route('/validate', methods=['POST'])
def validate_sensor_data():
    """
    Validate sensor data for model compatibility
    
    Expected input:
    {
        "sensor_data": [24 sensor values] or [[24 values], [24 values], ...]
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'sensor_data' not in data:
            return jsonify({'error': 'Missing sensor_data in request'}), 400
        
        sensor_data = np.array(data['sensor_data'])
        
        # Handle both single sample and batch
        if sensor_data.ndim == 1:
            sensor_data = sensor_data.reshape(1, -1)
        
        validation_results = {
            'is_valid': True,
            'issues': [],
            'data_info': {
                'shape': sensor_data.shape,
                'num_samples': sensor_data.shape[0],
                'num_features': sensor_data.shape[1]
            },
            'feature_analysis': {},
            'recommendations': []
        }
        
        # Check feature count
        expected_features = 24
        if sensor_data.shape[1] != expected_features:
            validation_results['is_valid'] = False
            validation_results['issues'].append(
                f'Expected {expected_features} features, got {sensor_data.shape[1]}'
            )
        
        # Check for invalid values
        if np.any(np.isnan(sensor_data)):
            validation_results['is_valid'] = False
            validation_results['issues'].append('Data contains NaN values')
        
        if np.any(np.isinf(sensor_data)):
            validation_results['is_valid'] = False
            validation_results['issues'].append('Data contains infinite values')
        
        # Feature analysis
        if sensor_data.shape[1] == expected_features:
            feature_names = []
            for i in range(1, 4):
                feature_names.append(f'setting_{i}')
            for i in range(1, 22):
                feature_names.append(f'sensor_{i}')
            
            for i, feature_name in enumerate(feature_names):
                if i < sensor_data.shape[1]:
                    feature_data = sensor_data[:, i]
                    validation_results['feature_analysis'][feature_name] = {
                        'mean': float(np.mean(feature_data)),
                        'std': float(np.std(feature_data)),
                        'min': float(np.min(feature_data)),
                        'max': float(np.max(feature_data)),
                        'range': float(np.max(feature_data) - np.min(feature_data))
                    }
                    
                    # Check for suspicious values
                    if np.std(feature_data) == 0:
                        validation_results['issues'].append(
                            f'{feature_name} has zero variance (constant values)'
                        )
                    
                    if abs(np.mean(feature_data)) > 10:
                        validation_results['recommendations'].append(
                            f'{feature_name} may need normalization (mean: {np.mean(feature_data):.2f})'
                        )
        
        # Overall data quality score
        quality_score = 100
        if validation_results['issues']:
            quality_score -= len(validation_results['issues']) * 20
        
        validation_results['quality_score'] = max(0, quality_score)
        validation_results['timestamp'] = datetime.utcnow().isoformat()
        validation_results['status'] = 'completed'
        
        return jsonify(validation_results)
        
    except Exception as e:
        logger.error(f"Data validation failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@data_bp.route('/load-dataset', methods=['POST'])
def load_dataset():
    """
    Load existing dataset from file
    
    Expected input:
    {
        "dataset_name": "turbofan_data_small.csv",
        "limit": 1000  # optional
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'dataset_name' not in data:
            return jsonify({'error': 'Missing dataset_name in request'}), 400
        
        dataset_name = data['dataset_name']
        limit = data.get('limit', None)
        
        # Validate dataset name
        allowed_datasets = [
            'turbofan_data_small.csv',
            'turbofan_data_medium.csv', 
            'turbofan_data_large.csv',
            'turbofan_train_small.csv',
            'turbofan_train_medium.csv',
            'turbofan_train_large.csv',
            'turbofan_test_small.csv',
            'turbofan_test_medium.csv',
            'turbofan_test_large.csv'
        ]
        
        if dataset_name not in allowed_datasets:
            return jsonify({
                'error': f'Dataset not found: {dataset_name}',
                'available_datasets': allowed_datasets
            }), 400
        
        # Construct file path - check both locations
        dataset_paths = [
            os.path.join('sample_datasets', dataset_name),
            os.path.join('data', 'sample_datasets', dataset_name),
            os.path.join('..', 'sample_datasets', dataset_name)
        ]
        
        dataset_path = None
        for path in dataset_paths:
            if os.path.exists(path):
                dataset_path = path
                break
        
        if not dataset_path:
            return jsonify({
                'error': f'Dataset file not found: {dataset_name}',
                'suggestion': 'Run python setup.py to generate datasets',
                'searched_paths': dataset_paths
            }), 404
        
        # Load dataset
        try:
            df = pd.read_csv(dataset_path)
            
            if limit and limit > 0:
                df = df.head(limit)
            
            # Convert to records
            records = df.to_dict('records')
            
            # Calculate statistics
            stats = {
                'total_records': len(df),
                'unique_engines': len(df['engine_id'].unique()) if 'engine_id' in df.columns else 0,
                'avg_rul': float(df['rul'].mean()) if 'rul' in df.columns else None,
                'max_rul': float(df['rul'].max()) if 'rul' in df.columns else None,
                'min_rul': float(df['rul'].min()) if 'rul' in df.columns else None,
                'columns': list(df.columns),
                'data_types': {col: str(df[col].dtype) for col in df.columns}
            }
            
            response = {
                'dataset_name': dataset_name,
                'records': records,
                'statistics': stats,
                'metadata': {
                    'loaded_at': datetime.utcnow().isoformat(),
                    'file_path': dataset_path,
                    'file_size_mb': round(os.path.getsize(dataset_path) / (1024*1024), 2)
                },
                'status': 'success'
            }
            
            return jsonify(response)
            
        except Exception as e:
            return jsonify({
                'error': f'Failed to load dataset: {str(e)}',
                'dataset_name': dataset_name
            }), 500
        
    except Exception as e:
        logger.error(f"Dataset loading failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@data_bp.route('/list-datasets', methods=['GET'])
def list_datasets():
    """List available datasets"""
    try:
        datasets_dir = os.path.join('data', 'sample_datasets')
        
        if not os.path.exists(datasets_dir):
            return jsonify({
                'datasets': [],
                'message': 'No datasets directory found. Run python setup.py to generate datasets.'
            })
        
        datasets = []
        for file in os.listdir(datasets_dir):
            if file.endswith('.csv'):
                file_path = os.path.join(datasets_dir, file)
                file_size = os.path.getsize(file_path)
                
                # Try to get record count
                try:
                    df = pd.read_csv(file_path, nrows=1)
                    total_rows = sum(1 for line in open(file_path)) - 1  # Subtract header
                except:
                    total_rows = 'unknown'
                
                datasets.append({
                    'name': file,
                    'size_mb': round(file_size / (1024*1024), 2),
                    'size_bytes': file_size,
                    'estimated_records': total_rows,
                    'modified': datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                })
        
        return jsonify({
            'datasets': datasets,
            'total_datasets': len(datasets),
            'datasets_directory': datasets_dir,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"List datasets failed: {str(e)}")
        return jsonify({'error': 'Internal server error', 'status': 'error'}), 500

@data_bp.route('/health', methods=['GET'])
def health_check():
    """Health check for data service"""
    try:
        # Test data generation
        test_df, _, _ = generate_synthetic_turbofan_data(10)
        
        return jsonify({
            'service': 'Data API',
            'status': 'healthy',
            'capabilities': [
                'sample_data_generation',
                'data_upload_validation',
                'data_preprocessing',
                'sensor_data_validation'
            ],
            'test_generation': {
                'samples_generated': len(test_df),
                'features_generated': len(test_df.columns)
            },
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'service': 'Data API',
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500
