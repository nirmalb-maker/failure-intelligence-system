import pandas as pd
import numpy as npgit 
import os
import re

def load_dataset():
    """
    Load the form_responses.csv dataset and preprocess it.
    """
    # Ensure absolute path regardless of where streamlit is run from
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "form_responses.csv")
    
    if not os.path.exists(file_path):
        print(f"Dataset not found at {file_path}")
        return pd.DataFrame()

    df = pd.read_csv(file_path)
    
    # Preprocess 'How many hours did you prepare?'
    def extract_hours(text):
        if pd.isna(text):
            return 0.0
        text = str(text).lower()
        
        # Handle specific text cases
        if 'year' in text:
            match = re.search(r'(\d+)\s*year', text)
            return float(match.group(1)) * 365 * 24 if match else 365 * 24.0
        if 'month' in text:
            match = re.search(r'(\d+)\s*month', text)
            return float(match.group(1)) * 30 * 24 if match else 30 * 24.0
        if 'day' in text:
            match = re.search(r'(\d+)\s*day', text)
            if match:
                 return float(match.group(1)) * 24.0
            elif 'daily' in text:
                 return 2.0 # Assumption for daily
            else:
                 return 24.0
                
        # Extract pure numbers anywhere else
        matches = re.findall(r'(\d+)', text)
        if matches:
            # If multiple numbers (e.g., 10-18), take average
            return sum(float(m) for m in matches) / len(matches)
        
        return 0.0
        
    df['Prep_Hours_Clean'] = df['How many hours did you prepare?'].apply(extract_hours)
    
    # Preprocess 'Confidence Level Before the Attempt'
    # It might contain text, but seems mostly numeric based on the schema
    df['Confidence_Clean'] = pd.to_numeric(df['Confidence Level Before the Attempt'], errors='coerce').fillna(5.0)
    
    # Fill empty Emotional State with mean if missing
    df['Emotional_State_Clean'] = pd.to_numeric(df['Emotional State After the Result'], errors='coerce').fillna(5.0)

    # Simplified cluster assignment based on Main Reason for Setback
    def assign_cluster(reason):
        reason = str(reason).lower()
        if 'anxiety' in reason or 'confidence' in reason or 'fear' in reason: return 0
        if 'knowledge' in reason or 'concept' in reason: return 1
        return 2 # Preparation Strategy Issue
        
        
    df['Cluster'] = df['What do you think was the main reason for the setback?'].apply(assign_cluster)
        
    # Map Failure Types to exactly the 5 allowed options
    allowed_types = ["Exam", "Interview", "Hackathon", "Internship / Job Application"]
    def map_failure_type(ft):
        ft = str(ft).strip()
        for allowed in allowed_types:
            # Simple substring or exact match. For exact match:
            if ft == allowed:
                return allowed
        # Also check if it's "Internship / Job Application" via substring just in case
        if "internship" in ft.lower() or "job" in ft.lower():
            return "Internship / Job Application"
        return "Other"
        
    if 'Failure Type' in df.columns:
        df['Failure Type'] = df['Failure Type'].apply(map_failure_type)
        
    return df

def get_failure_statistics(df=None):
    """
    Return basic metrics required for the dashboard.
    """
    if df is None:
        df = load_dataset()
        
    if df.empty:
        return 0, 0.0, 0.0
        
    total_failures = len(df)
    avg_confidence = df['Confidence_Clean'].mean()
    avg_prep_hours = df['Prep_Hours_Clean'].mean()
    
    return total_failures, avg_confidence, avg_prep_hours

def get_preparation_analysis(df=None):
    """
    Return filtered dataframe suitable for charting.
    """
    if df is None:
        df = load_dataset()
    return df
