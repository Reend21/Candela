# Application ID
app_id = 'org.reend.candela'

# Desktop file
desktop_file = configure_file(
  input: 'org.reend.candela.desktop.in',
  output: 'org.reend.candela.desktop',
  configuration: {
    'bindir': get_option('prefix') / get_option('bindir'),
  }
)

install_data(desktop_file,
  install_dir: get_option('datadir') / 'applications'
)

# Metainfo / AppStream
metainfo_file = files('org.reend.candela.metainfo.xml')

install_data(metainfo_file,
  install_dir: get_option('datadir') / 'metainfo'
)

# Icons - Install icons in various sizes
install_data('icons/hicolor/48x48/apps/org.reend.candela.png',
  install_dir: get_option('datadir') / 'icons/hicolor/48x48/apps'
)

install_data('icons/hicolor/64x64/apps/org.reend.candela.png',
  install_dir: get_option('datadir') / 'icons/hicolor/64x64/apps'
)

install_data('icons/hicolor/128x128/apps/org.reend.candela.png',
  install_dir: get_option('datadir') / 'icons/hicolor/128x128/apps'
)

install_data('icons/hicolor/scalable/apps/org.reend.candela.svg',
  install_dir: get_option('datadir') / 'icons/hicolor/scalable/apps'
)
