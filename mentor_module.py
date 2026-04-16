def generate_ai_advice(cluster, failure_type, description, confidence_level=5):
    """
    Simulates GPT-like responses based on the AI/ML detected cluster and failure type.
    """
    advice = {
        0: {
            "advice": "Confidence builds with practice and preparation. Based on what you described, you need to trust your abilities and avoid over-thinking in the moment.",
            "learning_suggestions": ["Try to visualize your success before starting a test.", "Start with easier problems to build momentum.", "Replace negative thoughts with positive affirmations."],
            "motivation": "A failure is just a stepping stone to success. Believe in yourself and keep pushing forward!"
        },
        1: {
            "advice": "Don't rush into complex problems. Make sure your base is strong before moving up. Reviewing the fundamentals is critical here.",
            "learning_suggestions": ["Try explaining what you just learned to an imaginary student. If you can't, review the material again.", "Revisit core concepts and foundational textbook chapters.", "Break down the most confusing topics into simple, discrete facts."],
            "motivation": "Every expert was once a beginner. Take it one step at a time, you are building your pyramid."
        },
        2: {
            "advice": "Rethink how you prepare. Time management and strategic studying are key. Passive reading isn't enough; you need active strategies.",
            "learning_suggestions": ["Use flashcards with spaced repetition to improve long-term retention.", "Break your tasks into 25-minute Pomodoro sessions and focus entirely on the task at hand.", "Create a realistic study schedule and adhere strictly to those deadlines."],
            "motivation": "Working smarter is often better than working harder. Find the right strategy, and results will follow."
        }
    }
    
    result = advice.get(cluster, advice[0]).copy()
    
    # Adjust for very low or high confidence
    if confidence_level <= 3:
        result["motivation"] = "Remember, self-doubt is normal. Take small steps and celebrate tiny wins. " + result["motivation"]
    elif confidence_level >= 8:
        result["motivation"] = "Channel that high confidence into executing the right strategy carefully. " + result["motivation"]
        
    if failure_type == "Internship / Job Application":
        result["advice"] += " Specifically for the job market, rejection is standard. It usually implies a mismatch rather than a personal deficiency."
        result["learning_suggestions"].extend([
            "Resume Improvement: Quantify your achievements and optimize for ATS.",
            "Interview Preparation: Do mock behavioral interviews using the STAR method.",
            "Portfolio Suggestions: Document one new end-to-end project on GitHub or your personal site."
        ])
        
    return result

