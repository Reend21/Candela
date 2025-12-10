"""
Birthday Row Widget - Custom row for displaying birthday entries.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject

from translations import _, get_month_names


class BirthdayRow(Adw.ActionRow):
    """A row widget for displaying a birthday entry."""
    
    __gtype_name__ = 'BirthdayRow'
    
    def __init__(self, birthday_data: dict, **kwargs):
        super().__init__(**kwargs)
        
        self.birthday_data = birthday_data
        self._setup_row()
        
    def _setup_row(self):
        """Set up the row display."""
        name = self.birthday_data.get('name', 'Unknown')
        day = self.birthday_data.get('day', 1)
        month = self.birthday_data.get('month', 1)
        year = self.birthday_data.get('year')
        days_until = self.birthday_data.get('days_until', 0)
        
        # Set title (name)
        self.set_title(name)
        
        # Format date using translated month names
        months = [''] + get_month_names()
        
        if year:
            date_str = f"{day} {months[month]} {year}"
        else:
            date_str = f"{day} {months[month]}"
        
        self.set_subtitle(date_str)
        
        # Days until badge
        if days_until == 0:
            days_text = _('today') + " 🎂"
        elif days_until == 1:
            days_text = _('tomorrow') + "!"
        else:
            days_text = _('days_left').format(days_until)
        
        days_label = Gtk.Label(label=days_text)
        days_label.add_css_class('dim-label')
        days_label.set_valign(Gtk.Align.CENTER)
        self.add_suffix(days_label)
        
        # Special icons for August 31 (Christmas tree and star)
        if day == 31 and month == 8:
            special_label = Gtk.Label(label="🎄⭐")
            special_label.set_valign(Gtk.Align.CENTER)
            self.add_suffix(special_label)
        
        # Add icon prefix (heart icon)
        icon = Gtk.Image.new_from_icon_name('emblem-favorite-symbolic')
        icon.set_valign(Gtk.Align.CENTER)
        icon.set_pixel_size(32)
        icon.add_css_class('birthday-heart-icon')
        self.add_prefix(icon)
        
        # Highlight upcoming birthdays (within 7 days)
        if days_until <= 7:
            self.add_css_class('upcoming-birthday')
            if days_until == 0:
                self.add_css_class('birthday-today')
        
        # Make row activatable
        self.set_activatable(True)
        
    def get_birthday_id(self) -> int:
        """Get the birthday ID."""
        return self.birthday_data.get('id', 0)
    
    def get_notes(self) -> str:
        """Get the birthday notes."""
        return self.birthday_data.get('notes', '')
    
    def get_birthday_data(self) -> dict:
        """Get the full birthday data."""
        return self.birthday_data
