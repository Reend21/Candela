"""
Data Manager - Handles persistent storage of event data.
"""

import json
import os
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional


# Event type constants
EVENT_TYPE_BIRTHDAY = 'birthday'
EVENT_TYPE_ANNIVERSARY = 'anniversary'
EVENT_TYPE_SPECIAL = 'special'

# Anniversary subtype constants
ANNIVERSARY_WEDDING = 'wedding'
ANNIVERSARY_RELATIONSHIP = 'relationship'
ANNIVERSARY_MEMORIAL = 'memorial'
ANNIVERSARY_OTHER = 'other'


class DataManager:
    """Manages event data storage and retrieval."""
    
    def __init__(self):
        # Use XDG_DATA_HOME for Flatpak compatibility
        xdg_data_home = os.environ.get('XDG_DATA_HOME', str(Path.home() / '.local' / 'share'))
        self.data_dir = Path(xdg_data_home) / 'candela'
        self.data_file = self.data_dir / 'events.json'
        self.legacy_data_file = self.data_dir / 'birthdays.json'
        self.settings_file = self.data_dir / 'settings.json'
        self._ensure_data_dir()
        self._migrate_legacy_data()
        
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def _migrate_legacy_data(self):
        """Migrate old birthdays.json to new events.json format."""
        if self.legacy_data_file.exists() and not self.data_file.exists():
            try:
                with open(self.legacy_data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    birthdays = data.get('birthdays', [])
                    
                # Convert to new format
                events = []
                for b in birthdays:
                    event = {
                        'id': b.get('id'),
                        'name': b.get('name'),
                        'day': b.get('day'),
                        'month': b.get('month'),
                        'year': b.get('year'),
                        'notes': b.get('notes', ''),
                        'event_type': EVENT_TYPE_BIRTHDAY,
                        'anniversary_type': None,
                        'created_at': b.get('created_at', datetime.now().isoformat())
                    }
                    events.append(event)
                
                self.save_events(events)
            except (json.JSONDecodeError, IOError):
                pass
        
    def load_events(self) -> List[Dict]:
        """Load all events from storage."""
        if not self.data_file.exists():
            return []
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('events', [])
        except (json.JSONDecodeError, IOError):
            return []
    
    # Legacy support
    def load_birthdays(self) -> List[Dict]:
        """Load all events (legacy support)."""
        return self.load_events()
    
    def save_events(self, events: List[Dict]):
        """Save events to storage."""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({'events': events}, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Error saving events: {e}")
    
    # Legacy support
    def save_birthdays(self, birthdays: List[Dict]):
        """Save events (legacy support)."""
        self.save_events(birthdays)
    
    def add_event(self, name: str, day: int, month: int, year: Optional[int] = None, 
                  notes: str = "", event_type: str = EVENT_TYPE_BIRTHDAY,
                  anniversary_type: Optional[str] = None) -> Dict:
        """Add a new event."""
        events = self.load_events()
        
        new_event = {
            'id': self._generate_id(events),
            'name': name,
            'day': day,
            'month': month,
            'year': year,
            'notes': notes,
            'event_type': event_type,
            'anniversary_type': anniversary_type,
            'created_at': datetime.now().isoformat()
        }
        
        events.append(new_event)
        self.save_events(events)
        return new_event
    
    # Legacy support
    def add_birthday(self, name: str, day: int, month: int, year: Optional[int] = None, notes: str = "") -> Dict:
        """Add a new birthday (legacy support)."""
        return self.add_event(name, day, month, year, notes, EVENT_TYPE_BIRTHDAY)
    
    def delete_event(self, event_id: int):
        """Delete an event by ID."""
        events = self.load_events()
        events = [e for e in events if e.get('id') != event_id]
        self.save_events(events)
    
    # Legacy support
    def delete_birthday(self, birthday_id: int):
        """Delete an event (legacy support)."""
        self.delete_event(birthday_id)
    
    def update_event(self, event_id: int, **kwargs):
        """Update an event."""
        events = self.load_events()
        for event in events:
            if event.get('id') == event_id:
                event.update(kwargs)
                break
        self.save_events(events)
    
    # Legacy support
    def update_birthday(self, birthday_id: int, **kwargs):
        """Update an event (legacy support)."""
        self.update_event(birthday_id, **kwargs)
    
    def _generate_id(self, events: List[Dict]) -> int:
        """Generate a unique ID for a new event."""
        if not events:
            return 1
        return max(e.get('id', 0) for e in events) + 1
    
    @staticmethod
    def days_until_event(day: int, month: int) -> int:
        """Calculate days until the next occurrence of an event."""
        today = date.today()
        try:
            this_year = date(today.year, month, day)
        except ValueError:
            # Handle invalid dates like Feb 30
            this_year = date(today.year, month, min(day, 28))
        
        if this_year < today:
            # Event already passed this year, calculate for next year
            try:
                next_year = date(today.year + 1, month, day)
            except ValueError:
                next_year = date(today.year + 1, month, min(day, 28))
            return (next_year - today).days
        else:
            return (this_year - today).days
    
    # Legacy support
    @staticmethod
    def days_until_birthday(day: int, month: int) -> int:
        """Calculate days until event (legacy support)."""
        return DataManager.days_until_event(day, month)
    
    @staticmethod
    def is_upcoming(day: int, month: int, days_threshold: int = 7) -> bool:
        """Check if an event is upcoming within the threshold."""
        days = DataManager.days_until_event(day, month)
        return days <= days_threshold
    
    def get_sorted_events(self) -> List[Dict]:
        """Get events sorted by days until next occurrence."""
        events = self.load_events()
        for e in events:
            e['days_until'] = self.days_until_event(e['day'], e['month'])
        return sorted(events, key=lambda x: x['days_until'])
    
    # Legacy support
    def get_sorted_birthdays(self) -> List[Dict]:
        """Get sorted events (legacy support)."""
        return self.get_sorted_events()
    
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
