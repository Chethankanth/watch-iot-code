"""
Machine Learning models for health data analysis
"""
import os
import numpy as np
import joblib
from pathlib import Path
from django.conf import settings

class HealthPredictor:
    """Class to handle all ML predictions for health data"""
    
    def __init__(self):
        """Initialize ML models"""
        # In a real application, you would load pre-trained models here
        # For this example, we'll simulate predictions
        self.fall_model = self._create_dummy_fall_model()
        self.vitals_model = self._create_dummy_vitals_model()
        
        # These would be the paths to your actual models
        # base_dir = Path(__file__).resolve().parent.parent
        # self.fall_model = joblib.load(os.path.join(base_dir, 'ml_models', 'fall_detection_model.pkl'))
        # self.vitals_model = joblib.load(os.path.join(base_dir, 'ml_models', 'vitals_risk_model.pkl'))
    
    def _create_dummy_fall_model(self):
        """Create a dummy fall detection model for demonstration"""
        class DummyFallModel:
            def predict_proba(self, X):
                """
                Simulate ML prediction - higher prediction for:
                - High acceleration values (sudden movements)
                - High gyroscope values (rapid rotation)
                """
                # X should have format [acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z]
                acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z = X[0]
                
                # Calculate acceleration magnitude
                acc_mag = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)
                
                # Calculate gyroscope magnitude
                gyr_mag = np.sqrt(gyr_x**2 + gyr_y**2 + gyr_z**2)
                
                # Fall detection logic
                # In a real system, this would be a trained model
                # Here we use a heuristic: high acceleration + high rotation = potential fall
                
                # Normal standing acceleration is around 9.8 m/s² (gravity)
                # If the acceleration is much different from gravity, it could be a fall
                gravity = 9.8
                acc_diff = abs(acc_mag - gravity)
                
                # Combine factors to get a probability
                # Higher values of both increase the probability
                fall_prob = min(0.95, (acc_diff * 0.15 + gyr_mag * 0.01))
                
                # Return probability matrix (for binary classification: not fall, fall)
                return np.array([[1 - fall_prob, fall_prob]])
        
        return DummyFallModel()
    
    def _create_dummy_vitals_model(self):
        """Create a dummy vitals risk model for demonstration"""
        class DummyVitalsModel:
            def predict_proba(self, X):
                """
                Simulate ML prediction based on heart rate and SpO2
                Normal ranges:
                - Heart rate: 60-100 bpm
                - SpO2: 95-100%
                """
                heart_rate, spo2 = X[0]
                
                # Calculate risk based on how far values are from normal ranges
                hr_risk = 0
                if heart_rate < 50:
                    hr_risk = (50 - heart_rate) * 0.05  # Bradycardia risk
                elif heart_rate > 100:
                    hr_risk = (heart_rate - 100) * 0.025  # Tachycardia risk
                
                spo2_risk = 0
                if spo2 < 95:
                    spo2_risk = (95 - spo2) * 0.1  # Hypoxemia risk
                
                # Combine risks (higher weight for SpO2 as it's more critical)
                total_risk = min(0.95, hr_risk + spo2_risk * 1.5)
                
                # Return probability matrix (for binary classification: normal, risk)
                return np.array([[1 - total_risk, total_risk]])
        
        return DummyVitalsModel()
    
    def predict_fall(self, acc_x, acc_y, acc_z, gyr_x, gyr_y, gyr_z):
        """
        Predict if a fall has occurred based on sensor data
        
        Args:
            acc_x, acc_y, acc_z: Accelerometer values
            gyr_x, gyr_y, gyr_z: Gyroscope values
            
        Returns:
            Dictionary with prediction results
        """
        # Prepare input data (using only the latest readings)
        X = np.array([[
            float(acc_x[-1]), float(acc_y[-1]), float(acc_z[-1]),
            float(gyr_x[-1]), float(gyr_y[-1]), float(gyr_z[-1])
        ]])
        
        # Make prediction
        prediction = self.fall_model.predict_proba(X)
        fall_probability = prediction[0][1]  # Probability of the positive class (fall)
        
        # Determine if it's an anomaly based on threshold
        threshold = 0.6  # Adjust based on your needs
        is_anomaly = fall_probability >= threshold
        
        return {
            'is_anomaly': is_anomaly,
            'fall_probability': fall_probability,
        }
    
    def predict_vitals_risk(self, heart_rate, spo2):
        """
        Predict health risk based on vital signs
        
        Args:
            heart_rate: Heart rate in BPM
            spo2: Blood oxygen saturation percentage
            
        Returns:
            Dictionary with prediction results
        """
        # Prepare input data
        X = np.array([[float(heart_rate), float(spo2)]])
        
        # Make prediction
        prediction = self.vitals_model.predict_proba(X)
        risk_probability = prediction[0][1]  # Probability of the positive class (risk)
        
        # Determine risk level based on probability
        if risk_probability < 0.3:
            risk_level = "NORMAL"
            is_anomaly = False
        elif risk_probability < 0.6:
            risk_level = "ELEVATED"
            is_anomaly = True
        elif risk_probability < 0.8:
            risk_level = "HIGH"
            is_anomaly = True
        else:
            risk_level = "CRITICAL"
            is_anomaly = True
        
        return {
            'is_anomaly': is_anomaly,
            'risk_probability': risk_probability,
            'risk_level': risk_level
        }