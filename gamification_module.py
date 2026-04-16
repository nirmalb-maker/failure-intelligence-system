def calculate_level(score):
    if score < 50:
        return "Beginner"
    elif score < 100:
        return "Learner"
    elif score < 200:
        return "Improver"
    else:
        return "Master"

def get_progress_to_next_level(score):
    if score < 50:
        return score / 50.0
    elif score < 100:
        return (score - 50) / 50.0
    elif score < 200:
        return (score - 100) / 100.0
    else:
        return 1.0
