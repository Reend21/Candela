"""
Event Row Widget - Custom row for displaying event entries with type-specific styling.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject

from translations import _, get_month_names
from data_manager import (EVENT_TYPE_BIRTHDAY, EVENT_TYPE_ANNIVERSARY, EVENT_TYPE_SPECIAL,
                          ANNIVERSARY_WEDDING, ANNIVERSARY_RELATIONSHIP, ANNIVERSARY_MEMORIAL, ANNIVERSARY_OTHER)


# Event type styling configuration
EVENT_STYLES = {
    EVENT_TYPE_BIRTHDAY: {
        'icon': 'emoji-food-symbolic',
        'emoji': '🎂',
        'css_class': 'event-birthday',
        'color': '#e66100',  # Orange
    },
    EVENT_TYPE_ANNIVERSARY: {
        ANNIVERSARY_WEDDING: {
            'icon': 'emblem-favorite-symbolic',
            'emoji': '💒',
            'css_class': 'event-anniversary-wedding',
            'color': '#d4af37',  # Gold
        },
        ANNIVERSARY_RELATIONSHIP: {
            'icon': 'emblem-favorite-symbolic',
            'emoji': '❤️',
            'css_class': 'event-anniversary-relationship', 
            'color': '#e91e63',  # Pink
        },
        ANNIVERSARY_MEMORIAL: {
            'icon': 'weather-clear-night-symbolic',
            'emoji': '🕯️',
            'css_class': 'event-anniversary-memorial',
            'color': '#1a1a1a',  # Black/Dark
        },
        ANNIVERSARY_OTHER: {
            'icon': 'x-office-calendar-symbolic',
            'emoji': '📅',
            'css_class': 'event-anniversary-other',
            'color': '#9c27b0',  # Purple
        },
    },
    EVENT_TYPE_SPECIAL: {
        'icon': 'starred-symbolic',
        'emoji': '⭐',
        'css_class': 'event-special',
        'color': '#2196f3',  # Blue
    },
}

# Holiday-specific styles (name-based detection)
HOLIDAY_STYLES = {
    # Christmas / Noel - Red & White
    'christmas': {
        'emoji': '🎄',
        'css_class': 'event-holiday-christmas',
        'color': '#c41e3a',  # Christmas Red
        'secondary_color': '#ffffff',  # White
    },
    'noel': {
        'emoji': '🎄',
        'css_class': 'event-holiday-christmas',
        'color': '#c41e3a',
        'secondary_color': '#ffffff',
    },
    # Halloween - Purple & Orange
    'halloween': {
        'emoji': '🎃',
        'css_class': 'event-holiday-halloween',
        'color': '#ff6600',  # Orange
        'secondary_color': '#6a0dad',  # Purple
    },
    'cadılar': {
        'emoji': '🎃',
        'css_class': 'event-holiday-halloween',
        'color': '#ff6600',
        'secondary_color': '#6a0dad',
    },
    # New Year - Gold & Silver
    'new_year': {
        'emoji': '🎆',
        'css_class': 'event-holiday-newyear',
        'color': '#ffd700',  # Gold
        'secondary_color': '#c0c0c0',  # Silver
    },
    'yılbaşı': {
        'emoji': '🎆',
        'css_class': 'event-holiday-newyear',
        'color': '#ffd700',
        'secondary_color': '#c0c0c0',
    },
    # Valentine's Day - Pink & Red
    'valentines': {
        'emoji': '💕',
        'css_class': 'event-holiday-valentines',
        'color': '#ff1493',  # Deep Pink
        'secondary_color': '#ff0000',  # Red
    },
    'sevgililer': {
        'emoji': '💕',
        'css_class': 'event-holiday-valentines',
        'color': '#ff1493',
        'secondary_color': '#ff0000',
    },
    # Ramadan - Green & Gold
    'ramadan': {
        'emoji': '🌙',
        'css_class': 'event-holiday-ramadan',
        'color': '#006400',  # Dark Green
        'secondary_color': '#ffd700',  # Gold
    },
    'ramazan': {
        'emoji': '🌙',
        'css_class': 'event-holiday-ramadan',
        'color': '#006400',
        'secondary_color': '#ffd700',
    },
    # Eid al-Adha / Kurban - Green & Gold
    'eid_al_adha': {
        'emoji': '🕌',
        'css_class': 'event-holiday-eid',
        'color': '#006400',
        'secondary_color': '#ffd700',
    },
    'kurban': {
        'emoji': '🕌',
        'css_class': 'event-holiday-eid',
        'color': '#006400',
        'secondary_color': '#ffd700',
    },
    # Easter - Pastel colors
    'easter': {
        'emoji': '🐰',
        'css_class': 'event-holiday-easter',
        'color': '#ff69b4',  # Hot Pink
        'secondary_color': '#87ceeb',  # Sky Blue
    },
    'paskalya': {
        'emoji': '🐰',
        'css_class': 'event-holiday-easter',
        'color': '#ff69b4',
        'secondary_color': '#87ceeb',
    },
    # Mother's Day - Pink
    'mothers_day': {
        'emoji': '💐',
        'css_class': 'event-holiday-mothers',
        'color': '#ff69b4',
    },
    'anneler': {
        'emoji': '💐',
        'css_class': 'event-holiday-mothers',
        'color': '#ff69b4',
    },
    # Father's Day - Blue
    'fathers_day': {
        'emoji': '👔',
        'css_class': 'event-holiday-fathers',
        'color': '#4169e1',  # Royal Blue
    },
    'babalar': {
        'emoji': '👔',
        'css_class': 'event-holiday-fathers',
        'color': '#4169e1',
    },
    # Thanksgiving - Brown & Orange
    'thanksgiving': {
        'emoji': '🦃',
        'css_class': 'event-holiday-thanksgiving',
        'color': '#8b4513',  # Saddle Brown
        'secondary_color': '#ff8c00',  # Dark Orange
    },
    'şükran': {
        'emoji': '🦃',
        'css_class': 'event-holiday-thanksgiving',
        'color': '#8b4513',
        'secondary_color': '#ff8c00',
    },
}


def get_holiday_style(name):
    """Check if the event name matches a known holiday and return its style."""
    name_lower = name.lower()
    for keyword, style in HOLIDAY_STYLES.items():
        if keyword.lower() in name_lower:
            return style
    return None


def get_event_style(event_type, anniversary_type=None, event_name=None):
    """Get the style configuration for an event type."""
    # First check if it's a known holiday by name
    if event_name:
        holiday_style = get_holiday_style(event_name)
        if holiday_style:
            return holiday_style
    
    # Then check by event type
    if event_type == EVENT_TYPE_ANNIVERSARY and anniversary_type:
        return EVENT_STYLES[EVENT_TYPE_ANNIVERSARY].get(anniversary_type, 
               EVENT_STYLES[EVENT_TYPE_ANNIVERSARY][ANNIVERSARY_OTHER])
    return EVENT_STYLES.get(event_type, EVENT_STYLES[EVENT_TYPE_SPECIAL])


class EventRow(Adw.ActionRow):
    """A row widget for displaying an event entry."""
    
    __gtype_name__ = 'EventRow'
    
    def __init__(self, event_data: dict, **kwargs):
        super().__init__(**kwargs)
        
        self.event_data = event_data
        self._setup_row()
        
    def _setup_row(self):
        """Set up the row display."""
        name = self.event_data.get('name', 'Unknown')
        day = self.event_data.get('day', 1)
        month = self.event_data.get('month', 1)
        year = self.event_data.get('year')
        days_until = self.event_data.get('days_until', 0)
        event_type = self.event_data.get('event_type', EVENT_TYPE_BIRTHDAY)
        anniversary_type = self.event_data.get('anniversary_type')
        
        # Get style for this event type (with name for holiday detection)
        style = get_event_style(event_type, anniversary_type, name)
        
        # Set title (name)
        self.set_title(name)
        
        # Format date using translated month names
        months = [''] + get_month_names()
        
        if year:
            date_str = f"{day} {months[month]} {year}"
        else:
            date_str = f"{day} {months[month]}"
        
        self.set_subtitle(date_str)
        
        # Days until badge with appropriate emoji
        if days_until == 0:
            days_text = _('today') + f" {style['emoji']}"
        elif days_until == 1:
            days_text = _('tomorrow') + "!"
        else:
            days_text = _('days_left').format(days_until)
        
        days_label = Gtk.Label(label=days_text)
        days_label.add_css_class('dim-label')
        days_label.set_valign(Gtk.Align.CENTER)
        self.add_suffix(days_label)
        
        # Show year count for events with year
        if year and event_type in [EVENT_TYPE_BIRTHDAY, EVENT_TYPE_ANNIVERSARY]:
            from datetime import date
            today = date.today()
            next_occurrence_year = today.year if days_until > 0 or (days_until == 0) else today.year
            if days_until > 0:
                # Check if the event is this year or next year
                try:
                    this_year_date = date(today.year, month, day)
                    if this_year_date < today:
                        next_occurrence_year = today.year + 1
                except ValueError:
                    pass
            
            years_count = next_occurrence_year - year
            if years_count > 0:
                if event_type == EVENT_TYPE_BIRTHDAY:
                    years_text = _('years_old').format(years_count)
                else:
                    years_text = _('anniversary_years').format(years_count)
                years_label = Gtk.Label(label=years_text)
                years_label.add_css_class('caption')
                years_label.add_css_class('dim-label')
                years_label.set_valign(Gtk.Align.CENTER)
                self.add_suffix(years_label)
        
        # Special icons for August 31 (Special date in original code)
        if day == 31 and month == 8:
            special_label = Gtk.Label(label="🎄⭐")
            special_label.set_valign(Gtk.Align.CENTER)
            self.add_suffix(special_label)
        
        # Add event type icon prefix
        icon_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        icon_box.set_valign(Gtk.Align.CENTER)
        
        # Use emoji for visual appeal
        emoji_label = Gtk.Label(label=style['emoji'])
        emoji_label.add_css_class('event-icon')
        icon_box.append(emoji_label)
        
        self.add_prefix(icon_box)
        
        # Add CSS classes for styling
        self.add_css_class('event-row')
        self.add_css_class(style['css_class'])
        
        # Highlight upcoming events (within 7 days)
        if days_until <= 7:
            self.add_css_class('upcoming-event')
            if days_until == 0:
                self.add_css_class('event-today')
        
        # Make row activatable
        self.set_activatable(True)
        
    def get_event_id(self) -> int:
        """Get the event ID."""
        return self.event_data.get('id', 0)
    
    # Legacy support
    def get_birthday_id(self) -> int:
        """Get the event ID (legacy support)."""
        return self.get_event_id()
    
    def get_notes(self) -> str:
        """Get the event notes."""
        return self.event_data.get('notes', '')
    
    def get_event_data(self) -> dict:
        """Get the full event data."""
        return self.event_data
    
    # Legacy support
    def get_birthday_data(self) -> dict:
        """Get the full event data (legacy support)."""
        return self.get_event_data()


# Legacy support - keep BirthdayRow as alias
class BirthdayRow(EventRow):
    """Legacy alias for EventRow."""
    __gtype_name__ = 'BirthdayRow'
