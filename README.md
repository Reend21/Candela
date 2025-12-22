<img width="256" height="256" alt="candela" src="https://github.com/user-attachments/assets/f5782853-b476-45ef-9a09-259c8d8aafcd" />

# Candela
Never forget your loved ones.

**Candela** is a simple adwaita app for not let you forget special days.
## Features

- 📅 Add birthdays, special days and events with optional year and notes
- ⏰ See days remaining until upcoming events
- 🌍 Multi-language support
- 💫 Simple interface with Adwaita

## Screenshots

*Coming soon...*

## Installation

### Flatpak (Recommended)

```bash
# Build and install locally
flatpak-builder --user --install --force-clean flatpak-build org.reend.candela.yml

# Run the application
flatpak run org.reend.candela
```

### From Source

#### Requirements
- Python 3.8+
- GTK4
- Libadwaita
- Meson
- Ninja

#### Build

```bash
# Configure
meson setup builddir --prefix=/usr/local

# Build
meson compile -C builddir

# Install
sudo meson install -C builddir

# Run
candela
```

## Development

### Running from Source

```bash
cd candela
python3 main.py
```

### Building Flatpak for Development

```bash
flatpak-builder --force-clean flatpak-build org.reend.candela.yml
```

## License

This project is licensed under the GPL-3.0-or-later License - see the [LICENSE](LICENSE) file for details.
