"""
Main Window - The primary application window.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio

from data_manager import DataManager
from birthday_row import BirthdayRow
from birthday_dialog import BirthdayDialog
from preferences import PreferencesWindow
from translations import _, set_language


class BirthdayWindow(Adw.ApplicationWindow):
    """Main application window."""
    
    __gtype_name__ = 'BirthdayWindow'
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.data_manager = DataManager()
        
        # Apply saved language first
        self._apply_saved_language()
        
        self.set_title(_('app_title'))
        self.set_default_size(400, 600)
        
        self._apply_saved_theme()
        self._setup_ui()
        self._load_birthdays()
        
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
        add_btn.set_tooltip_text(_('add_birthday'))
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
        
        # Cake icon
        cake_icon = Gtk.Image.new_from_icon_name("emblem-favorite-symbolic")
        cake_icon.set_pixel_size(128)
        cake_icon.add_css_class("cake-icon")
        empty_box.append(cake_icon)
        
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
        
        # Birthday list view
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
        
        # Top banner with cake icon
        banner_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        banner_box.set_halign(Gtk.Align.CENTER)
        banner_box.set_margin_bottom(12)
        
        banner_icon = Gtk.Image.new_from_icon_name("emblem-favorite-symbolic")
        banner_icon.set_pixel_size(160)
        banner_icon.add_css_class("cake-icon")
        banner_box.append(banner_icon)
        
        list_content.append(banner_box)
        
        # Birthday list group
        self.birthday_group = Adw.PreferencesGroup()
        self.birthday_group.set_title(_('all_birthdays'))
        self.birthday_group.add_css_class("birthday-group")
        
        self.birthday_listbox = Gtk.ListBox()
        self.birthday_listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.birthday_listbox.add_css_class("boxed-list")
        self.birthday_listbox.connect('row-activated', self._on_row_activated)
        
        self.birthday_group.add(self.birthday_listbox)
        list_content.append(self.birthday_group)
        
        scrolled.set_child(list_content)
        list_container.append(scrolled)
        
        self.content_stack.add_named(list_container, "list")
        
    def _load_birthdays(self):
        """Load and display birthdays."""
        # Clear existing rows
        while True:
            row = self.birthday_listbox.get_row_at_index(0)
            if row is None:
                break
            self.birthday_listbox.remove(row)
        
        # Get sorted birthdays
        birthdays = self.data_manager.get_sorted_birthdays()
        
        if not birthdays:
            self.content_stack.set_visible_child_name("empty")
            return
        
        self.content_stack.set_visible_child_name("list")
        
        # Add birthday rows
        for birthday in birthdays:
            row = BirthdayRow(birthday)
            self.birthday_listbox.append(row)
            
        # Update group title with count
        self.birthday_group.set_title(f"{_('all_birthdays')} ({len(birthdays)})")
        
    def _on_add_clicked(self, button):
        """Handle add button click."""
        dialog = BirthdayDialog()
        dialog.connect('birthday-added', self._on_birthday_added)
        dialog.present(self)
        
    def _on_birthday_added(self, dialog, name, day, month, year, notes):
        """Handle new birthday added."""
        self.data_manager.add_birthday(name, day, month, year, notes)
        self._load_birthdays()
        
        # Show toast
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
        
        # Update birthday group title
        birthdays = self.data_manager.get_sorted_birthdays()
        if birthdays:
            self.birthday_group.set_title(f"{_('all_birthdays')} ({len(birthdays)})")
        else:
            self.birthday_group.set_title(_('all_birthdays'))
        
        # Reload birthdays to update row texts
        self._load_birthdays()
        
    def _on_row_activated(self, listbox, row):
        """Handle row activation (for future edit/delete functionality)."""
        if isinstance(row, BirthdayRow):
            birthday_id = row.get_birthday_id()
            self._show_birthday_details(row, birthday_id)
            
    def _show_birthday_details(self, row, birthday_id):
        """Show birthday details with notes and delete option."""
        notes = row.get_notes()
        
        # Create dialog
        dialog = Adw.Dialog()
        dialog.set_title(_('birthday_details'))
        dialog.set_content_width(350)
        dialog.set_content_height(250)
        
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
        delete_btn.connect('clicked', self._on_delete_birthday, dialog, birthday_id, row.get_title())
        header.pack_start(delete_btn)
        
        main_box.append(header)
        
        # Content
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        content_box.set_margin_top(24)
        content_box.set_margin_bottom(24)
        content_box.set_margin_start(24)
        content_box.set_margin_end(24)
        
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
        
    def _on_delete_birthday(self, button, dialog, birthday_id, name):
        """Handle delete button click."""
        dialog.close()
        self.data_manager.delete_birthday(birthday_id)
        self._load_birthdays()
        
        toast = Adw.Toast.new(_('deleted_toast').format(name=name))
        toast.set_timeout(2)
        self.toast_overlay.add_toast(toast)
