#!/usr/bin/env python3
"""
Candela - Birthday Reminder Application
A GTK4 + Libadwaita application for tracking birthdays.
"""

import sys
import os
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, Gdk

from window import BirthdayWindow


class CandelaApp(Adw.Application):
    """Main application class."""
    
    def __init__(self):
        super().__init__(
            application_id='org.reend.candela',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        self.set_resource_base_path('/org/reend/candela')
        
    def do_startup(self):
        Adw.Application.do_startup(self)
        self._load_css()
        self._create_actions()
        
    def _load_css(self):
        """Load custom CSS styles."""
        css_provider = Gtk.CssProvider()
        
        # Try multiple paths for CSS file
        css_paths = [
            # Development path (running from source)
            os.path.join(os.path.dirname(os.path.abspath(__file__)), 'style.css'),
            # Flatpak installed path
            '/app/share/candela/style.css',
            # System installed path
            '/usr/share/candela/style.css',
            '/usr/local/share/candela/style.css',
            # Current directory (legacy)
            'style.css',
        ]
        
        css_loaded = False
        for css_path in css_paths:
            if os.path.exists(css_path):
                try:
                    css_provider.load_from_path(css_path)
                    css_loaded = True
                    break
                except Exception:
                    continue
        
        if css_loaded:
            Gtk.StyleContext.add_provider_for_display(
                Gdk.Display.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
        
    def _create_actions(self):
        """Create application actions."""
        quit_action = Gio.SimpleAction.new('quit', None)
        quit_action.connect('activate', lambda *_: self.quit())
        self.add_action(quit_action)
        self.set_accels_for_action('app.quit', ['<primary>q'])
        
    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = BirthdayWindow(application=self)
        win.present()


def main():
    app = CandelaApp()
    return app.run(sys.argv)


if __name__ == '__main__':
    sys.exit(main())

