#!/usr/bin/env python3
"""
Candela - Birthday Reminder Application
A GTK4 + Libadwaita application for tracking birthdays.
"""

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, Gdk

from window import BirthdayWindow


class CandelaApp(Adw.Application):
    """Main application class."""
    
    def __init__(self):
        super().__init__(
            application_id='com.github.candela',
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS
        )
        self.set_resource_base_path('/com/github/candela')
        
    def do_startup(self):
        Adw.Application.do_startup(self)
        self._load_css()
        self._create_actions()
        
    def _load_css(self):
        """Load custom CSS styles."""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('style.css')
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
