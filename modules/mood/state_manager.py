class MoodStateManager:
    def __init__(self):
        self.current_mood = "neutral"
        self.mood_intensity = 0.5
        self.mood_history = []
    
    def update_mood(self, new_mood, intensity=0.5, reason=None):
        self.current_mood = new_mood
        self.mood_intensity = intensity
        mood_entry = {
            "mood": new_mood,
            "intensity": intensity,
            "reason": reason,
            "timestamp": "2024-01-01T00:00:00"
        }
        self.mood_history.append(mood_entry)
        return self.get_mood_state()
    
    def get_mood_state(self):
        return {
            "current_mood": self.current_mood,
            "intensity": self.mood_intensity,
            "history_length": len(self.mood_history),
            "history": self.mood_history[-5:] if self.mood_history else []
        }
    
    def get_mood_trend(self):
        """Анализ тренда настроения"""
        if len(self.mood_history) < 2:
            return "stable"
        
        recent_moods = [entry["intensity"] for entry in self.mood_history[-3:]]
        if len(recent_moods) >= 2:
            if recent_moods[-1] > recent_moods[0]:
                return "improving"
            elif recent_moods[-1] < recent_moods[0]:
                return "declining"
        return "stable"