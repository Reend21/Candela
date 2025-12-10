"""
Preferences Window - Application settings.
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio

from data_manager import DataManager
from translations import _, set_language, get_language


BUILD_VERSION = "1.0.0"
BUILD_DATE = "2024-12-07"


class PreferencesWindow(Adw.PreferencesWindow):
    """Preferences window for application settings."""
    
    __gtype_name__ = 'PreferencesWindow'
    
    def __init__(self, data_manager: DataManager, on_language_changed=None, **kwargs):
        super().__init__(**kwargs)
        
        self.data_manager = data_manager
        self.settings = data_manager.load_settings()
        self.on_language_changed = on_language_changed
        
        self.set_title(_('preferences_title'))
        self.set_default_size(450, 500)
        self.set_modal(True)
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the preferences UI."""
        # Appearance page
        appearance_page = Adw.PreferencesPage()
        appearance_page.set_title(_('appearance'))
        appearance_page.set_icon_name("applications-graphics-symbolic")
        
        # Theme group
        theme_group = Adw.PreferencesGroup()
        theme_group.set_title(_('theme'))
        theme_group.set_description(_('theme_description'))
        
        # Theme combo row
        self.theme_row = Adw.ComboRow()
        self.theme_row.set_title(_('color_scheme'))
        self.theme_row.set_subtitle(_('color_scheme_subtitle'))
        
        theme_model = Gtk.StringList.new([_('system'), _('light'), _('dark')])
        self.theme_row.set_model(theme_model)
        
        # Set current theme
        theme_map = {'system': 0, 'light': 1, 'dark': 2}
        current_theme = self.settings.get('theme', 'system')
        self.theme_row.set_selected(theme_map.get(current_theme, 0))
        
        self.theme_row.connect('notify::selected', self._on_theme_changed)
        theme_group.add(self.theme_row)
        
        appearance_page.add(theme_group)
        
        # Language group
        lang_group = Adw.PreferencesGroup()
        lang_group.set_title(_('language'))
        lang_group.set_description(_('language_description'))
        
        # Language combo row
        self.lang_row = Adw.ComboRow()
        self.lang_row.set_title(_('language_selection'))
        self.lang_row.set_subtitle(_('language_subtitle'))
        
        lang_model = Gtk.StringList.new([_('auto'), _('turkish'), _('english'), _('spanish')])
        self.lang_row.set_model(lang_model)
        
        # Set current language
        lang_map = {'auto': 0, 'tr': 1, 'en': 2, 'es': 3}
        current_lang = self.settings.get('language', 'auto')
        self.lang_row.set_selected(lang_map.get(current_lang, 0))
        
        self.lang_row.connect('notify::selected', self._on_language_changed)
        lang_group.add(self.lang_row)
        
        appearance_page.add(lang_group)
        self.add(appearance_page)
        
        # Notifications page
        notifications_page = Adw.PreferencesPage()
        notifications_page.set_title(_('notifications'))
        notifications_page.set_icon_name("preferences-system-notifications-symbolic")
        
        # Notifications group
        notif_group = Adw.PreferencesGroup()
        notif_group.set_title(_('notification_settings'))
        notif_group.set_description(_('notification_description'))
        
        # Enable notifications switch
        self.notif_switch = Adw.SwitchRow()
        self.notif_switch.set_title(_('enable_notifications'))
        self.notif_switch.set_subtitle(_('enable_notifications_subtitle'))
        self.notif_switch.set_active(self.settings.get('notifications_enabled', True))
        self.notif_switch.connect('notify::active', self._on_notification_toggle)
        notif_group.add(self.notif_switch)
        
        # Days before notification
        self.days_row = Adw.SpinRow.new_with_range(1, 30, 1)
        self.days_row.set_title(_('reminder_days'))
        self.days_row.set_subtitle(_('reminder_days_subtitle'))
        self.days_row.set_value(self.settings.get('notification_days', 7))
        self.days_row.connect('notify::value', self._on_days_changed)
        notif_group.add(self.days_row)
        
        notifications_page.add(notif_group)
        self.add(notifications_page)
        
        # About page
        about_page = Adw.PreferencesPage()
        about_page.set_title(_('about'))
        about_page.set_icon_name("help-about-symbolic")
        
        # App info group
        info_group = Adw.PreferencesGroup()
        info_group.set_title(_('app_info'))
        
        # Version row
        version_row = Adw.ActionRow()
        version_row.set_title(_('version'))
        version_row.set_subtitle(BUILD_VERSION)
        version_row.add_prefix(Gtk.Image.new_from_icon_name("emblem-system-symbolic"))
        info_group.add(version_row)
        
        # Build date row
        build_row = Adw.ActionRow()
        build_row.set_title(_('build_date'))
        build_row.set_subtitle(BUILD_DATE)
        build_row.add_prefix(Gtk.Image.new_from_icon_name("x-office-calendar-symbolic"))
        info_group.add(build_row)
        
        # Developer row
        dev_row = Adw.ActionRow()
        dev_row.set_title(_('developer'))
        dev_row.set_subtitle("Reend")
        dev_row.add_prefix(Gtk.Image.new_from_icon_name("avatar-default-symbolic"))
        info_group.add(dev_row)
        
        # GitHub row
        github_row = Adw.ActionRow()
        github_row.set_title("GitHub")
        github_row.set_subtitle("github.com/Reend21")
        github_row.add_prefix(Gtk.Image.new_from_icon_name("web-browser-symbolic"))
        github_row.set_activatable(True)
        github_row.connect('activated', self._on_github_clicked)
        
        # Add arrow suffix to indicate it's clickable
        arrow = Gtk.Image.new_from_icon_name("go-next-symbolic")
        arrow.add_css_class("dim-label")
        github_row.add_suffix(arrow)
        info_group.add(github_row)
        
        about_page.add(info_group)
        
        # Credits group
        credits_group = Adw.PreferencesGroup()
        credits_group.set_title(_('technologies'))
        
        tech_row = Adw.ActionRow()
        tech_row.set_title(_('built_with'))
        tech_row.set_subtitle("Python • GTK4 • Libadwaita")
        tech_row.add_prefix(Gtk.Image.new_from_icon_name("applications-science-symbolic"))
        credits_group.add(tech_row)
        
        about_page.add(credits_group)
        self.add(about_page)
        
    def _on_theme_changed(self, row, _pspec):
        """Handle theme change."""
        selected = row.get_selected()
        theme_map = {0: 'system', 1: 'light', 2: 'dark'}
        theme = theme_map.get(selected, 'system')
        
        self.settings['theme'] = theme
        self.data_manager.save_settings(self.settings)
        
        # Apply theme
        style_manager = Adw.StyleManager.get_default()
        color_scheme_map = {
            'system': Adw.ColorScheme.DEFAULT,
            'light': Adw.ColorScheme.FORCE_LIGHT,
            'dark': Adw.ColorScheme.FORCE_DARK
        }
        style_manager.set_color_scheme(color_scheme_map.get(theme, Adw.ColorScheme.DEFAULT))
        
    def _on_language_changed(self, row, _pspec):
        """Handle language change."""
        selected = row.get_selected()
        lang_map = {0: 'auto', 1: 'tr', 2: 'en', 3: 'es'}
        lang = lang_map.get(selected, 'auto')
        
        self.settings['language'] = lang
        self.data_manager.save_settings(self.settings)
        
        # Apply language
        set_language(lang)
        
        # Notify parent to rebuild UI
        if self.on_language_changed:
            self.on_language_changed()
        
        # Close preferences and let user reopen to see changes
        self.close()
        
    def _on_notification_toggle(self, switch, _pspec):
        """Handle notification toggle."""
        self.settings['notifications_enabled'] = switch.get_active()
        self.data_manager.save_settings(self.settings)
        
    def _on_days_changed(self, row, _pspec):
        """Handle notification days change."""
        self.settings['notification_days'] = int(row.get_value())
        self.data_manager.save_settings(self.settings)
    
    def _on_github_clicked(self, row):
        """Open GitHub profile in browser."""
        Gtk.show_uri(self, "https://github.com/Reend21", 0)
