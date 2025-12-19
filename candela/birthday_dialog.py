"""
Event Dialog - Dialog for adding/editing events with type selection and quick holidays.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, GObject
from datetime import date

from translations import _
from data_manager import (EVENT_TYPE_BIRTHDAY, EVENT_TYPE_ANNIVERSARY, EVENT_TYPE_SPECIAL,
                          ANNIVERSARY_WEDDING, ANNIVERSARY_RELATIONSHIP, ANNIVERSARY_MEMORIAL, ANNIVERSARY_OTHER)


# Predefined holidays with their dates (month, day)
HOLIDAYS = {
    'new_year': {'month': 1, 'day': 1, 'icon': '🎆'},
    'valentines': {'month': 2, 'day': 14, 'icon': '💕'},
    'mothers_day': {'month': 5, 'day': 12, 'icon': '💐'},  # Second Sunday of May (approximate)
    'fathers_day': {'month': 6, 'day': 16, 'icon': '👔'},  # Third Sunday of June (approximate)
    'halloween': {'month': 10, 'day': 31, 'icon': '🎃'},
    'christmas': {'month': 12, 'day': 25, 'icon': '🎄'},
    'easter': {'month': 4, 'day': 20, 'icon': '🐰'},  # Variable date (approximate)
    'thanksgiving': {'month': 11, 'day': 28, 'icon': '🦃'},  # Fourth Thursday Nov (approximate)
    'ramadan': {'month': 4, 'day': 10, 'icon': '🌙'},  # Variable Islamic calendar
    'eid_al_adha': {'month': 6, 'day': 17, 'icon': '🕌'},  # Variable Islamic calendar
}


class EventDialog(Adw.Dialog):
    """Dialog for adding or editing an event."""
    
    __gtype_name__ = 'EventDialog'
    
    __gsignals__ = {
        'event-added': (GObject.SignalFlags.RUN_FIRST, None, (str, int, int, object, str, str, object)),
    }
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.set_title(_('new_event'))
        self.set_content_width(420)
        self.set_content_height(650)
        
        self.selected_event_type = EVENT_TYPE_BIRTHDAY
        self.selected_anniversary_type = None
        
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
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content.set_margin_top(16)
        content.set_margin_bottom(16)
        content.set_margin_start(16)
        content.set_margin_end(16)
        
        # Event Type Selection Group
        type_group = Adw.PreferencesGroup()
        type_group.set_title(_('event_type'))
        
        # Event type buttons in a box
        type_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        type_box.set_homogeneous(True)
        type_box.set_margin_top(8)
        type_box.set_margin_bottom(8)
        
        self.birthday_btn = Gtk.ToggleButton(label=f"🎂 {_('birthday')}")
        self.birthday_btn.set_active(True)
        self.birthday_btn.add_css_class('event-type-btn')
        self.birthday_btn.connect('toggled', self._on_type_toggled, EVENT_TYPE_BIRTHDAY)
        type_box.append(self.birthday_btn)
        
        self.anniversary_btn = Gtk.ToggleButton(label=f"💍 {_('anniversary')}")
        self.anniversary_btn.add_css_class('event-type-btn')
        self.anniversary_btn.connect('toggled', self._on_type_toggled, EVENT_TYPE_ANNIVERSARY)
        type_box.append(self.anniversary_btn)
        
        self.special_btn = Gtk.ToggleButton(label=f"⭐ {_('special_event')}")
        self.special_btn.add_css_class('event-type-btn')
        self.special_btn.connect('toggled', self._on_type_toggled, EVENT_TYPE_SPECIAL)
        type_box.append(self.special_btn)
        
        type_group.add(type_box)
        content.append(type_group)
        
        # Anniversary subtype group (hidden by default)
        self.anniversary_group = Adw.PreferencesGroup()
        self.anniversary_group.set_title(_('anniversary_type'))
        self.anniversary_group.set_visible(False)
        
        anniversary_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        anniversary_box.set_homogeneous(True)
        anniversary_box.set_margin_top(8)
        anniversary_box.set_margin_bottom(8)
        
        self.wedding_btn = Gtk.ToggleButton(label=f"💒 {_('wedding')}")
        self.wedding_btn.connect('toggled', self._on_anniversary_type_toggled, ANNIVERSARY_WEDDING)
        anniversary_box.append(self.wedding_btn)
        
        self.relationship_btn = Gtk.ToggleButton(label=f"❤️ {_('relationship')}")
        self.relationship_btn.connect('toggled', self._on_anniversary_type_toggled, ANNIVERSARY_RELATIONSHIP)
        anniversary_box.append(self.relationship_btn)
        
        self.memorial_btn = Gtk.ToggleButton(label=f"🕯️ {_('memorial')}")
        self.memorial_btn.connect('toggled', self._on_anniversary_type_toggled, ANNIVERSARY_MEMORIAL)
        anniversary_box.append(self.memorial_btn)
        
        self.other_ann_btn = Gtk.ToggleButton(label=f"📅 {_('other_anniversary')}")
        self.other_ann_btn.connect('toggled', self._on_anniversary_type_toggled, ANNIVERSARY_OTHER)
        anniversary_box.append(self.other_ann_btn)
        
        self.anniversary_group.add(anniversary_box)
        content.append(self.anniversary_group)
        
        # Quick Add Holidays Group (hidden by default, shown only for Special Event)
        self.holidays_group = Adw.PreferencesGroup()
        self.holidays_group.set_title(_('quick_add'))
        self.holidays_group.set_visible(False)
        
        # First row of holidays
        holidays_box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        holidays_box1.set_margin_top(8)
        holidays_box1.set_homogeneous(True)
        
        for holiday_key in ['new_year', 'christmas', 'valentines', 'halloween']:
            btn = Gtk.Button(label=f"{HOLIDAYS[holiday_key]['icon']} {_( holiday_key)}")
            btn.add_css_class('flat')
            btn.add_css_class('holiday-btn')
            btn.connect('clicked', self._on_holiday_clicked, holiday_key)
            holidays_box1.append(btn)
        
        self.holidays_group.add(holidays_box1)
        
        # Second row of holidays
        holidays_box2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        holidays_box2.set_margin_top(4)
        holidays_box2.set_margin_bottom(8)
        holidays_box2.set_homogeneous(True)
        
        for holiday_key in ['ramadan', 'eid_al_adha', 'mothers_day', 'fathers_day']:
            btn = Gtk.Button(label=f"{HOLIDAYS[holiday_key]['icon']} {_(holiday_key)}")
            btn.add_css_class('flat')
            btn.add_css_class('holiday-btn')
            btn.connect('clicked', self._on_holiday_clicked, holiday_key)
            holidays_box2.append(btn)
        
        self.holidays_group.add(holidays_box2)
        content.append(self.holidays_group)
        
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
    
    def _on_type_toggled(self, button, event_type):
        """Handle event type button toggle."""
        if button.get_active():
            self.selected_event_type = event_type
            
            # Deactivate other buttons
            if event_type != EVENT_TYPE_BIRTHDAY:
                self.birthday_btn.set_active(False)
            if event_type != EVENT_TYPE_ANNIVERSARY:
                self.anniversary_btn.set_active(False)
            if event_type != EVENT_TYPE_SPECIAL:
                self.special_btn.set_active(False)
            
            # Show/hide anniversary subtype
            self.anniversary_group.set_visible(event_type == EVENT_TYPE_ANNIVERSARY)
            
            # Show/hide holidays quick add (only for Special Event)
            self.holidays_group.set_visible(event_type == EVENT_TYPE_SPECIAL)
            
            if event_type != EVENT_TYPE_ANNIVERSARY:
                self.selected_anniversary_type = None
        else:
            # Don't allow deselecting the current type
            if self.selected_event_type == event_type:
                button.set_active(True)
    
    def _on_anniversary_type_toggled(self, button, ann_type):
        """Handle anniversary subtype button toggle."""
        if button.get_active():
            self.selected_anniversary_type = ann_type
            
            # Deactivate other buttons
            if ann_type != ANNIVERSARY_WEDDING:
                self.wedding_btn.set_active(False)
            if ann_type != ANNIVERSARY_RELATIONSHIP:
                self.relationship_btn.set_active(False)
            if ann_type != ANNIVERSARY_MEMORIAL:
                self.memorial_btn.set_active(False)
            if ann_type != ANNIVERSARY_OTHER:
                self.other_ann_btn.set_active(False)
    
    def _on_holiday_clicked(self, button, holiday_key):
        """Handle quick add holiday button click."""
        holiday = HOLIDAYS[holiday_key]
        
        # Set the name
        self.name_row.set_text(_(holiday_key))
        
        # Set the date on calendar
        today = date.today()
        try:
            from gi.repository import GLib
            holiday_date = GLib.DateTime.new_local(today.year, holiday['month'], holiday['day'], 0, 0, 0)
            self.calendar.select_day(holiday_date)
        except:
            pass
        
        # Set as special event
        self.special_btn.set_active(True)
        self.selected_event_type = EVENT_TYPE_SPECIAL
        
        # Don't include year for recurring holidays
        self.include_year.set_active(False)
        
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
        
        self.emit('event-added', name, day, month, year, notes, 
                  self.selected_event_type, self.selected_anniversary_type)
        self.close()


# Legacy support - keep BirthdayDialog as alias
class BirthdayDialog(EventDialog):
    """Legacy alias for EventDialog."""
    __gtype_name__ = 'BirthdayDialog'
    
    __gsignals__ = {
        'birthday-added': (GObject.SignalFlags.RUN_FIRST, None, (str, int, int, object, str)),
    }
    
    def _on_save_clicked(self, button):
        """Handle save button click with legacy signal."""
        name = self.name_row.get_text().strip()
        
        if not name:
            return
        
        calendar_date = self.calendar.get_date()
        day = calendar_date.get_day_of_month()
        month = calendar_date.get_month()
        year = calendar_date.get_year() if self.include_year.get_active() else None
        notes = self.notes_row.get_text().strip()
        
        self.emit('birthday-added', name, day, month, year, notes)
        self.close()
