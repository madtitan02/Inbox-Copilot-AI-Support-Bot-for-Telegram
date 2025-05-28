#!/usr/bin/env python3
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class ConversationHistory:
    def __init__(self, history_dir="conversation_history"):
        """Initialize conversation history manager"""
        self.history_dir = Path(history_dir)
        self.history_dir.mkdir(parents=True, exist_ok=True)
        self.current_session_file = self.history_dir / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        self.current_session = []
        
    def add_interaction(self, query: str, response: Dict[str, Any], confidence: int):
        """Add a query-response interaction to the current session"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response,
            "confidence": confidence
        }
        
        self.current_session.append(interaction)
        self._save_current_session()
        
    def _save_current_session(self):
        """Save the current session to file"""
        with open(self.current_session_file, 'w', encoding='utf-8') as f:
            json.dump(self.current_session, f, indent=2, ensure_ascii=False)
    
    def get_recent_interactions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recent interactions from current session"""
        return self.current_session[-limit:] if self.current_session else []
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session"""
        if not self.current_session:
            return {"total_queries": 0, "avg_confidence": 0, "topics": []}
        
        total_queries = len(self.current_session)
        avg_confidence = sum(interaction["confidence"] for interaction in self.current_session) / total_queries
        
        topics = []
        for interaction in self.current_session:
            query_words = interaction["query"].lower().split()
            topics.extend([word for word in query_words if len(word) > 3])
        
        topic_counts = {}
        for topic in topics:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        top_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "total_queries": total_queries,
            "avg_confidence": round(avg_confidence, 2),
            "topics": [topic for topic, count in top_topics],
            "session_file": str(self.current_session_file)
        }
    
    def search_history(self, search_term: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search through conversation history for relevant interactions"""
        matching_interactions = []
        
        for interaction in self.current_session:
            if search_term.lower() in interaction["query"].lower():
                matching_interactions.append(interaction)
        
        if len(matching_interactions) < limit:
            for session_file in self.history_dir.glob("session_*.json"):
                if session_file == self.current_session_file:
                    continue
                    
                try:
                    with open(session_file, 'r', encoding='utf-8') as f:
                        session_data = json.load(f)
                        
                    for interaction in session_data:
                        if search_term.lower() in interaction["query"].lower():
                            matching_interactions.append(interaction)
                            
                        if len(matching_interactions) >= limit:
                            break
                            
                except Exception as e:
                    print(f"Error reading session file {session_file}: {e}")
                    
                if len(matching_interactions) >= limit:
                    break
        
        return matching_interactions[:limit] 