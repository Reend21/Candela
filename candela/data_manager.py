"""
Data Manager - Handles persistent storage of birthday data.
"""

import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional


class DataManager:
    """Manages birthday data storage and retrieval."""
    
    def __init__(self):
        self.data_dir = Path.home() / '.local' / 'share' / 'birthday_app'
        self.data_file = self.data_dir / 'birthdays.json'
        self.settings_file = self.data_dir / 'settings.json'
        self._ensure_data_dir()
        
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def load_birthdays(self) -> List[Dict]:
        """Load all birthdays from storage."""
        if not self.data_file.exists():
            return []
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('birthdays', [])
        except (json.JSONDecodeError, IOError):
            return []
    
    def save_birthdays(self, birthdays: List[Dict]):
        """Save birthdays to storage."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({'birthdays': birthdays}, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving birthdays: {e}")
    
    def add_birthday(self, name: str, day: int, month: int, year: Optional[int] = None, notes: str = "") -> Dict:
        """Add a new birthday."""
        birthdays = self.load_birthdays()
        
        new_birthday = {
            'id': self._generate_id(birthdays),
            'name': name,
            'day': day,
            'month': month,
            'year': year,
            'notes': notes,
            'created_at': datetime.now().isoformat()
        }
        
        birthdays.append(new_birthday)
        self.save_birthdays(birthdays)
        return new_birthday
    
    def delete_birthday(self, birthday_id: int):
        """Delete a birthday by ID."""
        birthdays = self.load_birthdays()
        birthdays = [b for b in birthdays if b.get('id') != birthday_id]
        self.save_birthdays(birthdays)
    
    def update_birthday(self, birthday_id: int, **kwargs):
        """Update a birthday."""
        birthdays = self.load_birthdays()
        for birthday in birthdays:
            if birthday.get('id') == birthday_id:
                birthday.update(kwargs)
                break
        self.save_birthdays(birthdays)
    
    def _generate_id(self, birthdays: List[Dict]) -> int:
        """Generate a unique ID for a new birthday."""
        if not birthdays:
            return 1
        return max(b.get('id', 0) for b in birthdays) + 1
    
    @staticmethod
    def days_until_birthday(day: int, month: int) -> int:
        """Calculate days until the next occurrence of a birthday."""
        today = date.today()
        this_year = date(today.year, month, day)
        
        if this_year < today:
            # Birthday already passed this year, calculate for next year
            next_year = date(today.year + 1, month, day)
            return (next_year - today).days
        else:
            return (this_year - today).days
    
    @staticmethod
    def is_upcoming(day: int, month: int, days_threshold: int = 7) -> bool:
        """Check if a birthday is upcoming within the threshold."""
        days = DataManager.days_until_birthday(day, month)
        return days <= days_threshold
    
    def get_sorted_birthdays(self) -> List[Dict]:
        """Get birthdays sorted by days until next occurrence."""
        birthdays = self.load_birthdays()
        for b in birthdays:
            b['days_until'] = self.days_until_birthday(b['day'], b['month'])
        return sorted(birthdays, key=lambda x: x['days_until'])
    
    # Settings management
    def load_settings(self) -> Dict:
        """Load application settings."""
        default_settings = {
            'theme': 'system',  # 'system', 'light', 'dark'
            'notifications_enabled': True,
            'notification_days': 7
        }
        
        if not self.settings_file.exists():
            return default_settings
        
        try:
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                return {**default_settings, **settings}
        except (json.JSONDecodeError, IOError):
            return default_settings
    
    def save_settings(self, settings: Dict):
        """Save application settings."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving settings: {e}")
