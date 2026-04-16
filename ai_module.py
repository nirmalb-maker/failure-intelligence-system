import re
import os
from dotenv import load_dotenv

# Try importing openai, fallback if not available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()
def detect_failure_from_text(text, failure_type):
    """
    Use keyword-based NLP to detect failure patterns.
    Returns:
        tuple (cluster_id, detection_source_msg) or (None, detection_source_msg)
        
    Clusters:
    0 → Confidence Issue
    1 → Knowledge Gap
    2 → Preparation Problem
    """
    if not text:
        return None, "ML prediction used"

    text_lower = text.lower()
    
    # Keyword sets for each cluster
    confidence_keywords = ['confidence', 'anxiety', 'anxious', 'nervous', 'fear', 'panic', 'blanked', 'scared', 'doubt', 'overwhelmed']
    knowledge_keywords = ['knowledge', 'understand', 'concept', 'theory', 'blank', 'forgot', 'didn\'t know', 'did not know', 'hard', 'difficult', 'confused']
    preparation_keywords = ['time', 'plan', 'prepare', 'prepared', 'late', 'schedule', 'focus', 'distracted', 'procrastinate', 'rush', 'rushed']
    
    # Simple scoring mechanism
    scores = {
        0: sum(1 for word in confidence_keywords if word in text_lower),
        1: sum(1 for word in knowledge_keywords if word in text_lower),
        2: sum(1 for word in preparation_keywords if word in text_lower)
    }
    
    # Find the cluster with the highest score
    max_score = max(scores.values())
    if max_score > 0:
        # Get the first cluster with the max score (in case of tie, prioritize Confidence -> Knowledge -> Preparation)
        detected_cluster = [k for k, v in scores.items() if v == max_score][0]
        return detected_cluster, "AI detected pattern"
    
    # If no pattern detected strongly
    return None, "ML prediction used"


def generate_openai_mentor_response(messages, cluster, failure_type, description):
    """
    Calls the OpenAI API with the given chat messages and context.
    Streams the response back.
    Returns a tuple (stream_or_str, success_bool)
    """
    if not OPENAI_AVAILABLE:
        return "OpenAI library not installed.", False
        
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "API key not configured", False
        
    client = openai.OpenAI(api_key=api_key)
    
    # Construct base prompt based on context
    cluster_meanings = {
        0: "Confidence Issue (needs encouragement and practice strategies)",
        1: "Knowledge Gap (needs fundamental review and concepts breakdown)",
        2: "Preparation Problem (needs time management and study strategies)"
    }
    
    cluster_desc = cluster_meanings.get(cluster, "Unknown issue")
    
    system_prompt = f"""You are an intelligent, professional AI mentor for students/professionals facing failure or setbacks.
Your goal is to analyze their situation, provide structured, actionable steps, explain clearly, and motivate them.
Keep your responses concise but extremely helpful. Avoid generic advice; be specific to their issue.

User Context:
- Detected Issue Type: {cluster_desc}
- Self-Diagnosed Failure Type: {failure_type}
- User's Description of Failure: {description if description else "N/A"}
"""

    if failure_type == "Internship / Job Application":
        system_prompt += """
Domain-Specific Instructions for Job Applications:
- Include Resume improvement advice (e.g., ATS, action verbs).
- Include Interview preparation tips (e.g., STAR method).
- Include Portfolio/Networking suggestions.
"""

    formatted_messages = [{"role": "system", "content": system_prompt}]
    
    # Append the last 5-10 messages max
    recent_messages = messages[-10:] if len(messages) > 10 else messages
    
    # Format messages for OpenAI
    for msg in recent_messages:
        formatted_messages.append({"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]})
        
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", # or gpt-4 if preferred but 3.5 is faster and standard
            messages=formatted_messages,
            stream=True,
            temperature=0.7,
            max_tokens=800
        )
        return response, True
    except Exception as e:
        return f"OpenAI API Error: {str(e)}", False
