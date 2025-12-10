"""
Birthday Dialog - Dialog for adding/editing birthdays.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject
from datetime import date

from translations import _


class BirthdayDialog(Adw.Dialog):
    """Dialog for adding or editing a birthday."""
    
    __gtype_name__ = 'BirthdayDialog'
    
    __gsignals__ = {
        'birthday-added': (GObject.SignalFlags.RUN_FIRST, None, (str, int, int, object, str)),
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_title(_('new_birthday'))
        self.set_content_width(400)
        self.set_content_height(500)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the dialog UI."""
        # Main toolbar view
        toolbar_view = Adw.ToolbarView()
        self.set_child(toolbar_view)
        
        # Header bar
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(False)
        header.set_show_start_title_buttons(False)
        
        # Cancel button
        cancel_btn = Gtk.Button(label=_('cancel'))
        cancel_btn.connect('clicked', lambda _: self.close())
        header.pack_start(cancel_btn)
        
        # Save button
        save_btn = Gtk.Button(label=_('add'))
        save_btn.add_css_class('suggested-action')
        save_btn.connect('clicked', self._on_save_clicked)
        header.pack_end(save_btn)
        
        toolbar_view.add_top_bar(header)
        
        # Content
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        content.set_margin_top(24)
        content.set_margin_bottom(24)
        content.set_margin_start(24)
        content.set_margin_end(24)
        
        # Name entry group
        name_group = Adw.PreferencesGroup()
        name_group.set_title(_('name'))
        
        self.name_row = Adw.EntryRow()
        self.name_row.set_title(_('name_placeholder'))
        name_group.add(self.name_row)
        
        content.append(name_group)
        
        # Date selection group
        date_group = Adw.PreferencesGroup()
        date_group.set_title(_('date'))
        
        # Calendar
        calendar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        calendar_box.add_css_class('card')
        calendar_box.set_margin_top(8)
        
        self.calendar = Gtk.Calendar()
        self.calendar.set_margin_top(12)
        self.calendar.set_margin_bottom(12)
        self.calendar.set_margin_start(12)
        self.calendar.set_margin_end(12)
        calendar_box.append(self.calendar)
        
        # Year checkbox
        year_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        year_box.set_margin_start(12)
        year_box.set_margin_bottom(12)
        
        self.include_year = Gtk.CheckButton(label=_('year_optional'))
        self.include_year.set_active(True)
        year_box.append(self.include_year)
        calendar_box.append(year_box)
        
        date_group.add(calendar_box)
        content.append(date_group)
        
        # Notes group
        notes_group = Adw.PreferencesGroup()
        notes_group.set_title(_('notes'))
        
        self.notes_row = Adw.EntryRow()
        self.notes_row.set_title(_('notes_placeholder'))
        notes_group.add(self.notes_row)
        
        content.append(notes_group)
        
        # Scrolled window for content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_child(content)
        
        toolbar_view.set_content(scrolled)
        
    def _on_save_clicked(self, button):
        """Handle save button click."""
        name = self.name_row.get_text().strip()
        
        if not name:
            # Show error toast
            toast = Adw.Toast.new(_('name_placeholder'))
            # Find parent window and show toast
            return
        
        calendar_date = self.calendar.get_date()
        day = calendar_date.get_day_of_month()
        month = calendar_date.get_month()
        year = calendar_date.get_year() if self.include_year.get_active() else None
        notes = self.notes_row.get_text().strip()
        
        self.emit('birthday-added', name, day, month, year, notes)
        self.close()
