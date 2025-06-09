"""
Create a new vitals model that works with just 2 features (heart rate and SpO2)
"""
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
from pathlib import Path

# Define base directory
BASE_DIR = Path(__file__).resolve().parent

def create_sample_data():
    """Create sample data for model training"""
    # Create synthetic data for demonstration
    # Normal range: HR 60-100, SpO2 95-100
    # Moderate risk: HR 50-60 or 100-120, SpO2 90-95
    # High risk: HR < 50 or > 120, SpO2 < 90
    
    # Number of samples for each class
    n_normal = 500
    n_moderate = 300
    n_high = 200
    
    # Generate normal data
    normal_hr = np.random.uniform(60, 100, n_normal)
    normal_spo2 = np.random.uniform(95, 100, n_normal)
    normal_labels = ['Normal'] * n_normal
    
    # Generate moderate risk data - ensure equal sizes
    n_moderate_part = n_moderate // 3
    moderate_hr_low = np.random.uniform(50, 60, n_moderate_part)
    moderate_hr_high = np.random.uniform(100, 120, n_moderate_part)
    moderate_hr_mid = np.random.uniform(60, 100, n_moderate - 2*n_moderate_part)  # Handle division remainder
    moderate_hr = np.concatenate([moderate_hr_low, moderate_hr_high, moderate_hr_mid])
    
    n_moderate_half = n_moderate // 2
    moderate_spo2_low = np.random.uniform(90, 95, n_moderate_half)
    moderate_spo2_high = np.random.uniform(95, 100, n_moderate - n_moderate_half)  # Handle division remainder
    moderate_spo2 = np.concatenate([moderate_spo2_low, moderate_spo2_high])
    
    moderate_labels = ['Moderate'] * n_moderate
    
    # Generate high risk data - ensure equal sizes
    n_high_part = n_high // 3
    high_hr_low = np.random.uniform(30, 50, n_high_part)
    high_hr_high = np.random.uniform(120, 160, n_high_part)
    high_hr_mid = np.random.uniform(50, 120, n_high - 2*n_high_part)  # Handle division remainder
    high_hr = np.concatenate([high_hr_low, high_hr_high, high_hr_mid])
    
    n_high_half = n_high // 2
    high_spo2_low = np.random.uniform(70, 90, n_high_half)
    high_spo2_high = np.random.uniform(90, 95, n_high - n_high_half)  # Handle division remainder
    high_spo2 = np.concatenate([high_spo2_low, high_spo2_high])
    
    high_labels = ['High'] * n_high
    
    # Verify all lengths match before combining
    assert len(moderate_hr) == n_moderate, f"moderate_hr length {len(moderate_hr)} != {n_moderate}"
    assert len(moderate_spo2) == n_moderate, f"moderate_spo2 length {len(moderate_spo2)} != {n_moderate}"
    assert len(high_hr) == n_high, f"high_hr length {len(high_hr)} != {n_high}"
    assert len(high_spo2) == n_high, f"high_spo2 length {len(high_spo2)} != {n_high}"
    
    # Combine all data
    hr = np.concatenate([normal_hr, moderate_hr, high_hr])
    spo2 = np.concatenate([normal_spo2, moderate_spo2, high_spo2])
    labels = np.concatenate([normal_labels, moderate_labels, high_labels])
    
    # Verify final lengths match
    assert len(hr) == len(spo2), f"hr length {len(hr)} != spo2 length {len(spo2)}"
    assert len(hr) == len(labels), f"feature length {len(hr)} != labels length {len(labels)}"
    
    # Create feature matrix
    X = np.column_stack((hr, spo2))
    y = labels
    
    return X, y

def create_model(input_shape, num_classes):
    """Create LSTM model"""
    model = Sequential([
        LSTM(128, input_shape=input_shape, return_sequences=False),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dropout(0.2),
        Dense(num_classes, activation='softmax')
    ])
    
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

def main():
    print("Creating new vitals model for 2 features...")
    
    # Generate sample data
    X, y = create_sample_data()
    print(f"Generated {len(X)} samples with 2 features")
    
    # Encode labels
    encoder = LabelEncoder()
    y_encoded = encoder.fit_transform(y)
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Save encoder and scaler
    joblib.dump(encoder, os.path.join(BASE_DIR, 'vitals_encoder.pkl'))
    joblib.dump(scaler, os.path.join(BASE_DIR, 'vitals_scaler.pkl'))
    print("Saved encoder and scaler")
    
    # Create sequences for LSTM
    time_steps = 10
    n_features = X.shape[1]
    
    # Prepare LSTM sequences
    X_lstm = []
    y_lstm = []
    
    # For simplicity, create sequences by repeating each sample
    for i in range(len(X_scaled)):
        # Repeat the same values for time_steps
        seq = np.array([X_scaled[i]] * time_steps)
        X_lstm.append(seq)
        y_lstm.append(y_encoded[i])
    
    X_lstm = np.array(X_lstm)
    y_lstm = np.array(y_lstm)
    
    # Create and train model
    model = create_model((time_steps, n_features), len(encoder.classes_))
    
    print("Training model...")
    model.fit(
        X_lstm, y_lstm,
        epochs=10,
        batch_size=32,
        validation_split=0.2,
        verbose=1
    )
    
    # Save model
    model_path = os.path.join(BASE_DIR, 'vitals_model.keras')
    model.save(model_path)
    print(f"Model saved to {model_path}")
    
    print("\nVitals model has been created successfully!")
    print(f"Model input shape: {time_steps} time steps, {n_features} features")
    print(f"Model output: {len(encoder.classes_)} classes: {encoder.classes_}")
    print("\nYou can now use this model for vital signs analysis")
    
if __name__ == "__main__":
    main()