#!/usr/bin/env python3
"""
Sri Lankan SIM Swap Detection - ML Handler
Handles CSV/Excel upload, data cleaning, model training, and predictions
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Sri Lankan Cities
SRI_LANKAN_CITIES = [
    'Colombo', 'Gampaha', 'Kalutara', 'Kandy', 'Matale', 'Nuwara Eliya',
    'Galle', 'Matara', 'Hambantota', 'Jaffna', 'Kilinochchi', 'Mannar',
    'Vavuniya', 'Mullaitivu', 'Batticaloa', 'Ampara', 'Trincomalee',
    'Kurunegala', 'Puttalam', 'Anuradhapura', 'Polonnaruwa', 'Badulla',
    'Monaragala', 'Ratnapura', 'Kegalle'
]

class SriLankanMLHandler:
    """Handles ML operations for Sri Lankan SIM swap detection"""

    def __init__(self):
        self.df = None
        self.model = None
        self.scaler = None
        self.label_encoders = {}
        self.feature_columns = []
        self.model_path = 'sl_xgboost_model.pkl'
        self.scaler_path = 'sl_scaler.pkl'

    def load_dataset(self, file_path):
        """
        Load dataset from CSV or Excel file
        Supports UTF-8 encoding for Sinhala place names
        """
        try:
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension == '.csv':
                # Load CSV with UTF-8 encoding
                self.df = pd.read_csv(file_path, encoding='utf-8')
            elif file_extension in ['.xlsx', '.xls']:
                # Load Excel file
                self.df = pd.read_excel(file_path, engine='openpyxl')
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")

            # Clean the dataset
            self.clean_sri_lankan_data()

            return True
        except Exception as e:
            print(f"Error loading dataset: {e}")
            return False

    def clean_sri_lankan_data(self):
        """
        Clean Sri Lankan dataset
        - Strip whitespace from city names
        - Title case for cities
        - Ensure label is binary integer
        - Handle missing values
        """
        if self.df is None:
            return

        # Clean city columns
        city_columns = ['current_city', 'previous_city']
        for col in city_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip().str.title()

        # Ensure label is binary
        if 'label' in self.df.columns:
            self.df['label'] = self.df['label'].astype(int)

        # Handle missing values
        self.df = self.df.fillna(0)

        # Remove duplicates
        self.df = self.df.drop_duplicates()

    def get_dataset_preview(self, n_rows=10):
        """Get first n rows of dataset as dictionary"""
        if self.df is None:
            return None

        return self.df.head(n_rows).to_dict('records')

    def get_class_distribution(self):
        """Get distribution of classes (0 and 1)"""
        if self.df is None or 'label' not in self.df.columns:
            return None

        distribution = self.df['label'].value_counts().to_dict()
        return distribution

    def get_dataset_stats(self):
        """Get dataset statistics"""
        if self.df is None:
            return None

        return {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'columns': list(self.df.columns),
            'missing_values': self.df.isnull().sum().to_dict()
        }

    def prepare_features(self):
        """
        Prepare features for training
        - Encode categorical variables
        - Scale numerical features
        """
        if self.df is None:
            return False

        # Separate features and target
        if 'label' not in self.df.columns:
            raise ValueError("Dataset must have 'label' column")

        X = self.df.drop('label', axis=1)
        y = self.df['label']

        # Identify categorical and numerical columns
        categorical_cols = X.select_dtypes(include=['object']).columns
        numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns

        # Encode categorical variables
        for col in categorical_cols:
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col].astype(str))
            self.label_encoders[col] = le

        # Store feature columns
        self.feature_columns = list(X.columns)

        return X, y

    def train_model(self, model_type='xgboost', test_size=0.2, random_state=42):
        """
        Train ML model

        Args:
            model_type: 'xgboost', 'random_forest', or 'logistic'
            test_size: Proportion of test set
            random_state: Random seed

        Returns:
            Dictionary with metrics and confusion matrix
        """
        try:
            # Prepare features
            X, y = self.prepare_features()

            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=random_state, stratify=y
            )

            # Scale features
            self.scaler = StandardScaler()
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)

            # Select model
            if model_type == 'xgboost':
                self.model = XGBClassifier(
                    n_estimators=100,
                    max_depth=6,
                    learning_rate=0.1,
                    random_state=random_state,
                    eval_metric='logloss'
                )
            elif model_type == 'random_forest':
                self.model = RandomForestClassifier(
                    n_estimators=100,
                    max_depth=10,
                    random_state=random_state
                )
            elif model_type == 'logistic':
                self.model = LogisticRegression(
                    max_iter=1000,
                    random_state=random_state
                )
            else:
                raise ValueError(f"Unknown model type: {model_type}")

            # Train model
            self.model.fit(X_train_scaled, y_train)

            # Make predictions
            y_pred = self.model.predict(X_test_scaled)

            # Calculate metrics
            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall': recall_score(y_test, y_pred, zero_division=0),
                'f1_score': f1_score(y_test, y_pred, zero_division=0)
            }

            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)

            # Save model and scaler
            self.save_model()

            return {
                'status': 'success',
                'model_type': model_type,
                'metrics': metrics,
                'confusion_matrix': cm.tolist(),
                'features': self.feature_columns,
                'train_size': len(X_train),
                'test_size': len(X_test)
            }

        except Exception as e:
            print(f"Error training model: {e}")
            return {
                'status': 'error',
                'message': str(e)
            }

    def predict(self, data):
        """
        Make prediction on new data

        Args:
            data: Dictionary with feature values

        Returns:
            Dictionary with prediction and confidence
        """
        try:
            if self.model is None or self.scaler is None:
                raise ValueError("Model not trained. Please train model first.")

            # Create DataFrame from input data
            df_input = pd.DataFrame([data])

            # Ensure all feature columns are present
            for col in self.feature_columns:
                if col not in df_input.columns:
                    df_input[col] = 0

            # Reorder columns to match training
            df_input = df_input[self.feature_columns]

            # Encode categorical variables
            for col, le in self.label_encoders.items():
                if col in df_input.columns:
                    try:
                        df_input[col] = le.transform(df_input[col].astype(str))
                    except:
                        df_input[col] = 0

            # Scale features
            X_scaled = self.scaler.transform(df_input)

            # Make prediction
            prediction = self.model.predict(X_scaled)[0]

            # Get probability
            if hasattr(self.model, 'predict_proba'):
                proba = self.model.predict_proba(X_scaled)[0]
                confidence = proba[prediction]
            else:
                confidence = 1.0

            return {
                'status': 'success',
                'prediction': int(prediction),
                'confidence': float(confidence)
            }

        except Exception as e:
            print(f"Error making prediction: {e}")
            return {
                'status': 'error',
                'message': str(e),
                'prediction': 0,
                'confidence': 0.0
            }

    def save_model(self):
        """Save trained model and scaler to disk"""
        try:
            if self.model is not None:
                joblib.dump(self.model, self.model_path)
                print(f"✅ Model saved to {self.model_path}")

            if self.scaler is not None:
                joblib.dump(self.scaler, self.scaler_path)
                print(f"✅ Scaler saved to {self.scaler_path}")

            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False

    def load_model(self):
        """Load trained model and scaler from disk"""
        try:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
                print(f"✅ Model loaded from {self.model_path}")

            if os.path.exists(self.scaler_path):
                self.scaler = joblib.load(self.scaler_path)
                print(f"✅ Scaler loaded from {self.scaler_path}")

            return self.model is not None and self.scaler is not None
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
