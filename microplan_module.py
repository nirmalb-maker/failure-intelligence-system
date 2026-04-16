def generate_microplan(cluster, failure_type=None):
    plans = {
        0: {
            "issue": "Confidence Issue",
            "explanation": "Your failure seems connected to exam anxiety or a lack of confidence in your abilities.",
            "plan": [
                "Acknowledge your feelings and understand that anxiety is normal.",
                "Break down complex concepts into smaller, manageable pieces.",
                "Celebrate small wins and early successes to build momentum.",
                "Simulate real exam/test conditions to get used to the pressure.",
                "Talk to a mentor, peer, or counselor to gain perspective."
            ],
            "activities": [
                "Practice positive affirmations daily.",
                "Take timed mock tests under strict conditions.",
                "Engage in relaxation exercises (like deep breathing) before studying."
            ],
            "difficulty_score": 4
        },
        1: {
            "issue": "Knowledge Gap",
            "explanation": "There are fundamental concepts that you have not fully grasped yet.",
            "plan": [
                "Identify specific weak areas and outline them clearly.",
                "Gather elementary resources and foundational textbooks.",
                "Study the core principles deeply before moving to advanced topics.",
                "Do basic practice problems to ensure comprehension.",
                "Re-evaluate your understanding by teaching the concept to someone else."
            ],
            "activities": [
                "Review foundational textbooks from earlier courses.",
                "Watch explanatory videos on core topics.",
                "Teach the concept to an imaginary student."
            ],
            "difficulty_score": 5
        },
        2: {
            "issue": "Preparation Problem",
            "explanation": "You seem to struggle with prioritizing tasks, managing study time effectively, or aligning your prep with the exam format.",
            "plan": [
                "Identify key time wasters and limit your exposure to them.",
                "Block out dedicated study periods on your calendar.",
                "Use a timer (Pomodoro technique) during study sessions to maintain focus.",
                "Regularly test yourself instead of passively reading.",
                "Adapt your strategy continuously based on practice results."
            ],
            "activities": [
                "Create a detailed weekly study schedule.",
                "Use the Pomodoro technique for uninterrupted focus.",
                "Switch to active recall and spaced repetition flashcards."
            ],
            "difficulty_score": 4
        }
    }
    
    plan_data = plans.get(cluster, plans[0]).copy()
    
    if failure_type == "Internship / Job Application":
        plan_data["issue"] = "Career Opportunity Setback"
        plan_data["explanation"] = "Your setback is related to professional opportunities, which require career-focused improvements."
        plan_data["plan"] = [
            "Review and refine your resume significantly.",
            "Schedule mock behavioral and technical interviews.",
            "Build or update an end-to-end portfolio project.",
            "Attend a networking event or connect directly on LinkedIn.",
            "Follow up professionally on all future applications."
        ]
        plan_data["activities"] = [
            "Update your resume to quantify achievements.",
            "Practice technical and behavioral interviews (STAR method).",
            "Develop a new portfolio project to showcase skills.",
            "Reach out to an industry professional for networking or a coffee chat."
        ]
        
    return plan_data
