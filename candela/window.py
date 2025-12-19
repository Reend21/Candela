"""
Main Window - The primary application window.
"""

import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GdkPixbuf

from data_manager import DataManager
from birthday_row import EventRow, BirthdayRow
from birthday_dialog import EventDialog, BirthdayDialog
from preferences import PreferencesWindow
from translations import _, set_language


def get_icon_path():
    """Find the application icon file path."""
    # Always use candela-symbolic.png for main screen icon
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'candela-symbolic.png')
    if os.path.exists(icon_path):
        return icon_path
    return None


class CandelaWindow(Adw.ApplicationWindow):
    """Main application window."""
    
    __gtype_name__ = 'CandelaWindow'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.data_manager = DataManager()
        
        # Apply saved language first
        self._apply_saved_language()
        
        self.set_title(_('app_title'))
        self.set_default_size(420, 650)
        
        self._apply_saved_theme()
        self._setup_ui()
        self._load_events()
        
    def _apply_saved_language(self):
        """Apply the saved language setting."""
        settings = self.data_manager.load_settings()
        lang = settings.get('language', 'auto')
        set_language(lang)
        
    def _apply_saved_theme(self):
        """Apply the saved theme setting."""
        settings = self.data_manager.load_settings()
        theme = settings.get('theme', 'system')
        
        style_manager = Adw.StyleManager.get_default()
        color_scheme_map = {
            'system': Adw.ColorScheme.DEFAULT,
            'light': Adw.ColorScheme.FORCE_LIGHT,
            'dark': Adw.ColorScheme.FORCE_DARK
        }
        style_manager.set_color_scheme(color_scheme_map.get(theme, Adw.ColorScheme.DEFAULT))
        
    def _setup_ui(self):
        """Set up the main UI."""
        # Main box
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.main_box)
        
        # Header bar
        header = Adw.HeaderBar()
        
        # Add button (left)
        add_btn = Gtk.Button()
        add_btn.set_icon_name("list-add-symbolic")
        add_btn.set_tooltip_text(_('add_event'))
        add_btn.add_css_class("flat")
        add_btn.connect('clicked', self._on_add_clicked)
        header.pack_start(add_btn)
        
        # Settings button (right)
        settings_btn = Gtk.Button()
        settings_btn.set_icon_name("emblem-system-symbolic")
        settings_btn.set_tooltip_text(_('settings'))
        settings_btn.add_css_class("flat")
        settings_btn.connect('clicked', self._on_settings_clicked)
        header.pack_end(settings_btn)
        
        self.main_box.append(header)
        
        # Toast overlay for notifications
        self.toast_overlay = Adw.ToastOverlay()
        self.main_box.append(self.toast_overlay)
        
        # Content stack (for empty state vs list)
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
        self.content_stack.set_vexpand(True)
        self.toast_overlay.set_child(self.content_stack)
        
        # Empty state
        empty_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        empty_box.set_valign(Gtk.Align.CENTER)
        empty_box.set_halign(Gtk.Align.CENTER)
        
        # App logo icon
        icon_path = get_icon_path()
        if icon_path:
            logo_icon = Gtk.Image.new_from_file(icon_path)
        else:
            logo_icon = Gtk.Image.new_from_icon_name("emblem-favorite-symbolic")
        logo_icon.set_pixel_size(128)
        logo_icon.add_css_class("app-icon")
        empty_box.append(logo_icon)
        
        # Empty state title
        self.empty_title = Gtk.Label(label=_('empty_title'))
        self.empty_title.add_css_class("empty-state-title")
        self.empty_title.add_css_class("title-1")
        empty_box.append(self.empty_title)
        
        # Empty state subtitle
        self.empty_subtitle = Gtk.Label(label=_('empty_subtitle'))
        self.empty_subtitle.add_css_class("empty-state-subtitle")
        self.empty_subtitle.set_justify(Gtk.Justification.CENTER)
        empty_box.append(self.empty_subtitle)
        
        self.content_stack.add_named(empty_box, "empty")
        
        # Event list view
        list_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Scrolled window for the list
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        
        # Main content box inside scrolled
        list_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        list_content.set_margin_top(12)
        list_content.set_margin_bottom(12)
        list_content.set_margin_start(12)
        list_content.set_margin_end(12)
        
        # Top banner with logo icon
        banner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        banner_box.set_halign(Gtk.Align.CENTER)
        banner_box.set_margin_bottom(12)
        
        icon_path = get_icon_path()
        if icon_path:
            banner_icon = Gtk.Image.new_from_file(icon_path)
        else:
            banner_icon = Gtk.Image.new_from_icon_name("emblem-favorite-symbolic")
        banner_icon.set_pixel_size(160)
        banner_icon.add_css_class("app-icon")
        banner_box.append(banner_icon)
        
        list_content.append(banner_box)
        
        # Upcoming events list group (within 7 days)
        self.upcoming_group = Adw.PreferencesGroup()
        self.upcoming_group.set_title(_('upcoming_events'))
        self.upcoming_group.add_css_class("upcoming-group")
        
        self.upcoming_listbox = Gtk.ListBox()
        self.upcoming_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.upcoming_listbox.add_css_class("boxed-list")
        self.upcoming_listbox.connect('row-activated', self._on_row_activated)
        
        self.upcoming_group.add(self.upcoming_listbox)
        list_content.append(self.upcoming_group)
        
        # All events list group
        self.events_group = Adw.PreferencesGroup()
        self.events_group.set_title(_('all_events'))
        self.events_group.add_css_class("events-group")
        
        self.events_listbox = Gtk.ListBox()
        self.events_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.events_listbox.add_css_class("boxed-list")
        self.events_listbox.connect('row-activated', self._on_row_activated)
        
        self.events_group.add(self.events_listbox)
        list_content.append(self.events_group)
        
        scrolled.set_child(list_content)
        list_container.append(scrolled)
        
        self.content_stack.add_named(list_container, "list")
        
    def _load_events(self):
        """Load and display events."""
        # Clear existing rows from both listboxes
        while True:
            row = self.upcoming_listbox.get_row_at_index(0)
            if row is None:
                break
            self.upcoming_listbox.remove(row)
            
        while True:
            row = self.events_listbox.get_row_at_index(0)
            if row is None:
                break
            self.events_listbox.remove(row)
        
        # Get sorted events
        events = self.data_manager.get_sorted_events()
        
        if not events:
            self.content_stack.set_visible_child_name("empty")
            return
        
        self.content_stack.set_visible_child_name("list")
        
        # Separate upcoming events (within 7 days) from others
        upcoming_events = []
        other_events = []
        
        for event in events:
            days_until = event.get('days_until', 999)
            if days_until <= 7:
                upcoming_events.append(event)
            else:
                other_events.append(event)
        
        # Add upcoming event rows
        for event in upcoming_events:
            row = EventRow(event)
            self.upcoming_listbox.append(row)
        
        # Add other event rows
        for event in other_events:
            row = EventRow(event)
            self.events_listbox.append(row)
        
        # Update group titles with counts
        if upcoming_events:
            self.upcoming_group.set_title(f"{_('upcoming_events')} ({len(upcoming_events)})")
            self.upcoming_group.set_visible(True)
        else:
            self.upcoming_group.set_visible(False)
        
        if other_events:
            self.events_group.set_title(f"{_('all_events')} ({len(other_events)})")
            self.events_group.set_visible(True)
        else:
            self.events_group.set_visible(False)
    
    # Legacy support
    def _load_birthdays(self):
        """Load events (legacy support)."""
        self._load_events()
        
    def _on_add_clicked(self, button):
        """Handle add button click."""
        dialog = EventDialog()
        dialog.connect('event-added', self._on_event_added)
        dialog.present(self)
        
    def _on_event_added(self, dialog, name, day, month, year, notes, event_type, anniversary_type):
        """Handle new event added."""
        self.data_manager.add_event(name, day, month, year, notes, event_type, anniversary_type)
        self._load_events()
        
        # Show toast
        toast = Adw.Toast.new(_('added_toast').format(name=name))
        toast.set_timeout(2)
        self.toast_overlay.add_toast(toast)
    
    # Legacy support
    def _on_birthday_added(self, dialog, name, day, month, year, notes):
        """Handle new birthday added (legacy support)."""
        self.data_manager.add_birthday(name, day, month, year, notes)
        self._load_events()
        
        toast = Adw.Toast.new(_('added_toast').format(name=name))
        toast.set_timeout(2)
        self.toast_overlay.add_toast(toast)
        
    def _on_settings_clicked(self, button):
        """Handle settings button click."""
        prefs = PreferencesWindow(
            self.data_manager, 
            on_language_changed=self._on_language_changed,
            transient_for=self
        )
        prefs.present()
        
    def _on_language_changed(self):
        """Handle language change - rebuild UI."""
        # Update window title
        self.set_title(_('app_title'))
        
        # Update empty state texts
        self.empty_title.set_label(_('empty_title'))
        self.empty_subtitle.set_label(_('empty_subtitle'))
        
        # Reload events to update row texts and group titles
        self._load_events()
        
    def _on_row_activated(self, listbox, row):
        """Handle row activation (for edit/delete functionality)."""
        if isinstance(row, (EventRow, BirthdayRow)):
            event_id = row.get_event_id()
            self._show_event_details(row, event_id)
            
    def _show_event_details(self, row, event_id):
        """Show event details with notes and delete option."""
        notes = row.get_notes()
        event_data = row.get_event_data()
        
        # Create dialog
        dialog = Adw.Dialog()
        dialog.set_title(_('event_details'))
        dialog.set_content_width(350)
        dialog.set_content_height(280)
        
        # Main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        dialog.set_child(main_box)
        
        # Header bar
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(True)
        header.set_show_start_title_buttons(False)
        
        # Delete button with trash icon
        delete_btn = Gtk.Button()
        delete_btn.set_icon_name("user-trash-symbolic")
        delete_btn.add_css_class("destructive-action")
        delete_btn.set_tooltip_text(_('delete'))
        delete_btn.connect('clicked', self._on_delete_event, dialog, event_id, row.get_title(), event_data)
        header.pack_start(delete_btn)
        
        main_box.append(header)
        
        # Content
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        
        # Event type indicator
        event_type = event_data.get('event_type', 'birthday')
        anniversary_type = event_data.get('anniversary_type')
        
        from birthday_row import get_event_style
        event_name = event_data.get('name', '')
        style = get_event_style(event_type, anniversary_type, event_name)
        
        type_label = Gtk.Label(label=f"{style['emoji']} {_(event_type)}")
        type_label.add_css_class("caption")
        type_label.add_css_class("dim-label")
        content_box.append(type_label)
        
        # Name label
        name_label = Gtk.Label(label=row.get_title())
        name_label.add_css_class("title-1")
        content_box.append(name_label)
        
        # Date label
        date_label = Gtk.Label(label=row.get_subtitle())
        date_label.add_css_class("dim-label")
        content_box.append(date_label)
        
        # Notes section
        notes_frame = Gtk.Frame()
        notes_frame.set_margin_top(8)
        
        notes_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        notes_box.set_margin_top(12)
        notes_box.set_margin_bottom(12)
        notes_box.set_margin_start(12)
        notes_box.set_margin_end(12)
        
        notes_title = Gtk.Label(label=_('notes'))
        notes_title.add_css_class("heading")
        notes_title.set_halign(Gtk.Align.START)
        notes_box.append(notes_title)
        
        if notes and notes.strip():
            notes_content = Gtk.Label(label=notes)
        else:
            notes_content = Gtk.Label(label=_('no_notes'))
            notes_content.add_css_class("dim-label")
        
        notes_content.set_wrap(True)
        notes_content.set_halign(Gtk.Align.START)
        notes_box.append(notes_content)
        
        notes_frame.set_child(notes_box)
        content_box.append(notes_frame)
        
        main_box.append(content_box)
        
        dialog.present(self)
    
    # Legacy support  
    def _show_birthday_details(self, row, birthday_id):
        """Show event details (legacy support)."""
        self._show_event_details(row, birthday_id)
        
    def _on_delete_event(self, button, dialog, event_id, name, event_data=None):
        """Handle delete button click."""
        dialog.close()
        self.data_manager.delete_event(event_id)
        self._load_events()
        
        # Easter egg: special toast messages based on event type
        toast_message = _('deleted_toast').format(name=name)
        
        if event_data:
            from data_manager import (EVENT_TYPE_ANNIVERSARY, ANNIVERSARY_MEMORIAL, 
                                       ANNIVERSARY_WEDDING, ANNIVERSARY_RELATIONSHIP)
            event_type = event_data.get('event_type')
            anniversary_type = event_data.get('anniversary_type')
            
            if event_type == EVENT_TYPE_ANNIVERSARY:
                if anniversary_type == ANNIVERSARY_MEMORIAL:
                    # Easter egg: memorial deletion shows just "..."
                    toast_message = _('deleted_memorial_toast')
                elif anniversary_type in [ANNIVERSARY_WEDDING, ANNIVERSARY_RELATIONSHIP]:
                    # Easter egg: love anniversary deletion shows special message
                    toast_message = _('deleted_love_toast')
        
        toast = Adw.Toast.new(toast_message)
        toast.set_timeout(2)
        self.toast_overlay.add_toast(toast)
    
    # Legacy support
    def _on_delete_birthday(self, button, dialog, birthday_id, name):
        """Handle delete (legacy support)."""
        self._on_delete_event(button, dialog, birthday_id, name)


# Legacy support - keep BirthdayWindow as alias
class BirthdayWindow(CandelaWindow):
    """Legacy alias for CandelaWindow."""
    __gtype_name__ = 'BirthdayWindow'
