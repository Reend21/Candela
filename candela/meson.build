# Python sources
python_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'birthday_dialog.py',
  'birthday_row.py',
  'data_manager.py',
  'preferences.py',
  'translations.py',
]

# Install Python modules
install_data(python_sources,
  install_dir: get_option('prefix') / get_option('datadir') / 'candela'
)

# Install CSS
install_data('style.css',
  install_dir: get_option('prefix') / get_option('datadir') / 'candela'
)

# Install app icon for runtime access
install_data('../data/icons/hicolor/128x128/apps/org.reend.candela.png',
  install_dir: get_option('prefix') / get_option('datadir') / 'candela',
  rename: 'org.reend.candela.png'
)

# Create launcher script
launcher_conf = configuration_data()
launcher_conf.set('PYTHON', python.find_installation('python3').full_path())
launcher_conf.set('pkgdatadir', get_option('prefix') / get_option('datadir') / 'candela')
launcher_conf.set('localedir', get_option('prefix') / get_option('localedir'))
launcher_conf.set('VERSION', meson.project_version())

configure_file(
  input: 'candela.in',
  output: 'candela',
  configuration: launcher_conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)
