<img width="256" height="256" alt="candela" src="https://github.com/user-attachments/assets/f5782853-b476-45ef-9a09-259c8d8aafcd" />

# Candela
<<<<<<< Updated upstream
An Adwaita app to take notes for your relatives birthday.
=======

<p align="center">
  <img src="data/icons/hicolor/128x128/apps/org.reend.candela.png" alt="Candela Logo" width="128">
</p>

**Candela** is a beautiful and simple birthday reminder application built with GTK4 and Libadwaita.
Keep track of your loved ones' birthdays and never forget to wish them a happy birthday.

## Features

- 📅 Add birthdays with optional year and notes
- ⏰ See days remaining until upcoming birthdays
- 🎨 Highlight upcoming birthdays with accent color
- 🌍 Multi-language support (English, Turkish, Spanish)
- 🌙 Light and dark theme support
- 💫 Modern and beautiful interface

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

## Author

**Reend** - [GitHub](https://github.com/Reend21)
>>>>>>> Stashed changes
