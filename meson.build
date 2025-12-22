project('candela',
  version: '1.0.0',
  meson_version: '>= 0.59.0',
  default_options: ['warning_level=2', 'werror=false']
)

# Application ID
app_id = 'org.reend.candela'

# Directories
prefix = get_option('prefix')
bindir = prefix / get_option('bindir')
datadir = prefix / get_option('datadir')
pkgdatadir = datadir / meson.project_name()

# Python
python = import('python')
py_installation = python.find_installation('python3')

# Dependencies check (info only, actual deps are Python runtime)
# These are only for validation - the actual deps are provided by Flatpak runtime
dependency('glib-2.0', version: '>= 2.66', required: false)
dependency('gtk4', version: '>= 4.6', required: false)
dependency('libadwaita-1', version: '>= 1.0', required: false)

# GSettings schema compiler for future use
gnome = import('gnome')

# Subdirectories
subdir('data')
subdir('candela')

# Post-install script to update icon cache
gnome.post_install(
  gtk_update_icon_cache: true,
  update_desktop_database: true,
)
