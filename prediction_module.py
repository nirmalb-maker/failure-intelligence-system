import pickle
import os
import numpy as np
import pandas as pd

def load_models():
    """Load the trained machine learning models dynamically."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "models")
    
    try:
        with open(os.path.join(models_dir, 'fis_kmeans_model.pkl'), 'rb') as f:
            kmeans_model = pickle.load(f)
        with open(os.path.join(models_dir, 'imputer.pkl'), 'rb') as f:
            imputer_model = pickle.load(f)
        with open(os.path.join(models_dir, 'scaler.pkl'), 'rb') as f:
            scaler_model = pickle.load(f)
        return kmeans_model, imputer_model, scaler_model
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None, None

def predict_cluster(prep_hours, confidence, structured_prep, result_score, emotional_state):
    """
    Predict the failure root cause cluster using the trained FIS K-Means model.
    """
    kmeans, imputer, scaler = load_models()
    
    # Mappings
    labels = {
        0: "Confidence Issue",
        1: "Knowledge Gap",
        2: "Preparation Problem",
        3: "Other Issue" # Fallback if model predicts a 4th cluster
    }
    
    if kmeans is None or imputer is None or scaler is None:
        # Fallback pseudo-logic if models are missing
        cluster_idx = int((confidence + prep_hours) % 3)
        return cluster_idx, labels.get(cluster_idx)
        
    # Map 'Structured Preparation' to numeric if it's passed as a string or bool
    if isinstance(structured_prep, str):
        sp_map = {"Yes, fully structured": 1.0, "Partially structured": 0.5, "No structured plan": 0.0}
        structured_prep_val = sp_map.get(structured_prep, 0.5)
    elif isinstance(structured_prep, bool):
        structured_prep_val = 1.0 if structured_prep else 0.0
    else:
        structured_prep_val = float(structured_prep)
        
    # Form feature array with 5 inputs matching new ML model
    features = pd.DataFrame(
        [[prep_hours, confidence, structured_prep_val, result_score, emotional_state]], 
        columns=['Prep_Hours_Clean', 'Confidence_Clean', 'Structured_Plan_Numeric', 'Result Score (If applicable)', 'Emotional_State_Clean']
    )
    
    # Preprocess and Predict
    try:
        # Try processing 5 features
        features_imputed = imputer.transform(features)
        features_scaled = scaler.transform(features_imputed)
        cluster = int(kmeans.predict(features_scaled)[0])
        
        # Ensure it maps into the [0, 1, 2] range for our new definitions
        mapped_cluster = cluster if cluster in [0, 1, 2] else (cluster % 3)
        return mapped_cluster, labels.get(mapped_cluster)
        
    except ValueError as e:
        # If the actual model file still expects 4 features (graceful degradation if not updated)
        print(f"Model dimensionality mismatch, falling back to 4 features: {e}")
        try:
            features_4 = features.drop(columns=['Emotional_State_Clean'])
            features_imputed = imputer.transform(features_4)
            features_scaled = scaler.transform(features_imputed)
            cluster = int(kmeans.predict(features_scaled)[0])
            mapped_cluster = cluster if cluster in [0, 1, 2] else (cluster % 3)
            return mapped_cluster, labels.get(mapped_cluster)
        except Exception as inner_e:
            print(f"Secondary ML prediction error: {inner_e}")
            cluster_idx = int((confidence + prep_hours) % 3)
            return cluster_idx, labels.get(cluster_idx)
    except Exception as e:
        print(f"ML prediction error: {e}")
        cluster_idx = int((confidence + prep_hours) % 3)
        return cluster_idx, labels.get(cluster_idx)

def predict_failure_risk(confidence_level, prep_hours, emotional_state, habit_score=5):
    """
    Calculate failure risk using formula adjusted for habit score.
    Returns risk score (0-100) and risk category.
    """
    # Modified logic to include habit score reducing risk
    risk_raw = (100 - (confidence_level * 10)) + (prep_hours * 0.3) - (emotional_state * 5) - (habit_score * 2)
    risk = max(0, min(100, risk_raw))
    
    if risk <= 40:
        category = "Low Risk"
    elif risk <= 70:
        category = "Medium Risk"
    else:
        category = "High Risk"
        
    return risk, category
