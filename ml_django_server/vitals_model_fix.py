"""
Fix script to modify the vitals model scaler to work with 2 features
"""
import os
import sys
import numpy as np
import joblib
from pathlib import Path

# Define base directory
BASE_DIR = Path(__file__).resolve().parent

def main():
    print("Examining vitals scaler...")
    
    # Load the existing scaler
    scaler_path = os.path.join(BASE_DIR, 'vitals_scaler.pkl')
    try:
        scaler = joblib.load(scaler_path)
        print(f"Loaded scaler from {scaler_path}")
        
        # Check scaler properties
        print(f"Scaler n_features_in_: {scaler.n_features_in_}")
        print(f"Scaler mean_: {scaler.mean_}")
        print(f"Scaler scale_: {scaler.scale_}")
        
        # Create a new scaler with just 2 features (assuming the first 2 are HR and SpO2)
        scaler.n_features_in_ = 2
        if len(scaler.mean_) > 2:
            scaler.mean_ = scaler.mean_[:2]
        if len(scaler.scale_) > 2:
            scaler.scale_ = scaler.scale_[:2]
        if hasattr(scaler, 'var_') and len(scaler.var_) > 2:
            scaler.var_ = scaler.var_[:2]
            
        print("\nUpdated scaler properties:")
        print(f"Scaler n_features_in_: {scaler.n_features_in_}")
        print(f"Scaler mean_: {scaler.mean_}")
        print(f"Scaler scale_: {scaler.scale_}")
        
        # Save the updated scaler
        backup_path = scaler_path + '.backup'
        joblib.dump(scaler, backup_path)
        print(f"Saved backup of original scaler to {backup_path}")
        
        joblib.dump(scaler, scaler_path)
        print(f"Saved updated scaler to {scaler_path}")
        
        print("\nScaler has been updated to work with 2 features (heart rate and SpO2)")
        return True
    except Exception as e:
        print(f"Error updating scaler: {e}")
        return False

if __name__ == "__main__":
    main()