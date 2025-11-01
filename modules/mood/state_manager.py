class MoodStateManager:
    def __init__(self):
        self.current_mood = "neutral"
        self.mood_intensity = 0.5
        self.mood_history = []

    def update_mood(self, new_mood, intensity=0.5):
        self.current_mood = new_mood
        self.mood_intensity = intensity
        self.mood_history.append({
            "mood": new_mood,
            "intensity": intensity,
            "timestamp": "2024-01-01T00:00:00"
        })
        return self.get_mood_state()

    def get_mood_state(self):
        return {
            "current_mood": self.current_mood,
            "intensity": self.mood_intensity,
            "history_length": len(self.mood_history)
        }