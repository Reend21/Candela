"""
Translations - Internationalization support for Candela.
"""

import locale

# Translation dictionaries
TRANSLATIONS = {
    'tr': {
        # Window
        'app_title': 'Candela',
        'add_birthday': 'Doğum Günü Ekle',
        'settings': 'Ayarlar',
        
        # Empty state
        'empty_title': 'Henüz bir doğum günü eklemedin, o kadar mı yalnızsın?',
        'empty_subtitle': 'Yeni bir doğum günü eklemek için\n+ butonuna tıklayın',
        
        # Birthday list
        'all_birthdays': 'Tüm Doğum Günleri',
        'today': 'Bugün!',
        'tomorrow': 'Yarın',
        'days_left': '{} gün kaldı',
        'was_days_ago': '{} gün önce',
        'years_old': '{} yaşına giriyor',
        
        # Birthday dialog
        'new_birthday': 'Yeni Doğum Günü',
        'name': 'İsim',
        'name_placeholder': 'Kişinin adını girin',
        'date': 'Tarih',
        'day': 'Gün',
        'month': 'Ay',
        'year': 'Yıl',
        'year_optional': 'Yıl (isteğe bağlı)',
        'notes': 'Notlar',
        'notes_placeholder': 'İsteğe bağlı notlar',
        'cancel': 'İptal',
        'add': 'Ekle',
        
        # Months
        'january': 'Ocak',
        'february': 'Şubat',
        'march': 'Mart',
        'april': 'Nisan',
        'may': 'Mayıs',
        'june': 'Haziran',
        'july': 'Temmuz',
        'august': 'Ağustos',
        'september': 'Eylül',
        'october': 'Ekim',
        'november': 'Kasım',
        'december': 'Aralık',
        
        # Birthday options
        'birthday_options_body': 'Bu doğum günü için ne yapmak istersiniz?',
        'delete': 'Sil',
        'no_notes': 'Not eklenmemiş',
        'birthday_details': 'Doğum Günü Detayları',
        
        # Toasts
        'added_toast': "'{name}' eklendi",
        'deleted_toast': "'{name}' silindi",
        
        # Preferences
        'preferences_title': 'Ayarlar',
        'appearance': 'Görünüm',
        'theme': 'Tema',
        'theme_description': 'Uygulama temasını seçin',
        'color_scheme': 'Renk Şeması',
        'color_scheme_subtitle': 'Uygulamanın görünüm temasını belirler',
        'system': 'Sistem',
        'light': 'Açık',
        'dark': 'Koyu',
        
        # Language
        'language': 'Dil',
        'language_description': 'Uygulama dilini seçin',
        'language_selection': 'Dil Seçimi',
        'language_subtitle': 'Uygulamanın dilini belirler',
        'auto': 'Otomatik (Sistem)',
        'turkish': 'Türkçe',
        'english': 'English',
        'spanish': 'Español',
        
        # Notifications
        'notifications': 'Bildirimler',
        'notification_settings': 'Bildirim Ayarları',
        'notification_description': 'Doğum günü hatırlatıcılarını yapılandırın',
        'enable_notifications': 'Bildirimleri Etkinleştir',
        'enable_notifications_subtitle': 'Yaklaşan doğum günleri için bildirim al',
        'reminder_days': 'Hatırlatma Günü',
        'reminder_days_subtitle': 'Doğum gününden kaç gün önce bildirim gönderilsin',
        
        # About
        'about': 'Hakkında',
        'app_info': 'Uygulama Bilgisi',
        'version': 'Sürüm',
        'build_date': 'Yapım Tarihi',
        'developer': 'Geliştirici',
        'technologies': 'Teknolojiler',
        'built_with': 'Yapılış',
    },
    'en': {
        # Window
        'app_title': 'Candela',
        'add_birthday': 'Add Birthday',
        'settings': 'Settings',
        
        # Empty state
        'empty_title': "You haven't added any birthdays yet, are you that lonely?",
        'empty_subtitle': 'Click the + button\nto add a new birthday',
        
        # Birthday list
        'all_birthdays': 'All Birthdays',
        'today': 'Today!',
        'tomorrow': 'Tomorrow',
        'days_left': '{} days left',
        'was_days_ago': '{} days ago',
        'years_old': 'Turning {}',
        
        # Birthday dialog
        'new_birthday': 'New Birthday',
        'name': 'Name',
        'name_placeholder': "Enter person's name",
        'date': 'Date',
        'day': 'Day',
        'month': 'Month',
        'year': 'Year',
        'year_optional': 'Year (optional)',
        'notes': 'Notes',
        'notes_placeholder': 'Optional notes',
        'cancel': 'Cancel',
        'add': 'Add',
        
        # Months
        'january': 'January',
        'february': 'February',
        'march': 'March',
        'april': 'April',
        'may': 'May',
        'june': 'June',
        'july': 'July',
        'august': 'August',
        'september': 'September',
        'october': 'October',
        'november': 'November',
        'december': 'December',
        
        # Birthday options
        'birthday_options_body': 'What would you like to do with this birthday?',
        'delete': 'Delete',
        'no_notes': 'No notes added',
        'birthday_details': 'Birthday Details',
        
        # Toasts
        'added_toast': "'{name}' added",
        'deleted_toast': "'{name}' deleted",
        
        # Preferences
        'preferences_title': 'Settings',
        'appearance': 'Appearance',
        'theme': 'Theme',
        'theme_description': 'Choose the application theme',
        'color_scheme': 'Color Scheme',
        'color_scheme_subtitle': 'Sets the appearance theme of the application',
        'system': 'System',
        'light': 'Light',
        'dark': 'Dark',
        
        # Language
        'language': 'Language',
        'language_description': 'Choose the application language',
        'language_selection': 'Language Selection',
        'language_subtitle': 'Sets the language of the application',
        'auto': 'Automatic (System)',
        'turkish': 'Türkçe',
        'english': 'English',
        'spanish': 'Español',
        
        # Notifications
        'notifications': 'Notifications',
        'notification_settings': 'Notification Settings',
        'notification_description': 'Configure birthday reminders',
        'enable_notifications': 'Enable Notifications',
        'enable_notifications_subtitle': 'Get notified about upcoming birthdays',
        'reminder_days': 'Reminder Days',
        'reminder_days_subtitle': 'Days before birthday to send notification',
        
        # About
        'about': 'About',
        'app_info': 'Application Info',
        'version': 'Version',
        'build_date': 'Build Date',
        'developer': 'Developer',
        'technologies': 'Technologies',
        'built_with': 'Built with',
    },
    'es': {
        # Window
        'app_title': 'Candela',
        'add_birthday': 'Agregar Cumpleaños',
        'settings': 'Configuración',
        
        # Empty state
        'empty_title': '¿Todavía no has añadido ningún cumpleaños, tan solo estás?',
        'empty_subtitle': 'Haz clic en el botón +\npara agregar un nuevo cumpleaños',
        
        # Birthday list
        'all_birthdays': 'Todos los Cumpleaños',
        'today': '¡Hoy!',
        'tomorrow': 'Mañana',
        'days_left': 'Faltan {} días',
        'was_days_ago': 'Hace {} días',
        'years_old': 'Cumple {}',
        
        # Birthday dialog
        'new_birthday': 'Nuevo Cumpleaños',
        'name': 'Nombre',
        'name_placeholder': 'Ingrese el nombre de la persona',
        'date': 'Fecha',
        'day': 'Día',
        'month': 'Mes',
        'year': 'Año',
        'year_optional': 'Año (opcional)',
        'notes': 'Notas',
        'notes_placeholder': 'Notas opcionales',
        'cancel': 'Cancelar',
        'add': 'Agregar',
        
        # Months
        'january': 'Enero',
        'february': 'Febrero',
        'march': 'Marzo',
        'april': 'Abril',
        'may': 'Mayo',
        'june': 'Junio',
        'july': 'Julio',
        'august': 'Agosto',
        'september': 'Septiembre',
        'october': 'Octubre',
        'november': 'Noviembre',
        'december': 'Diciembre',
        
        # Birthday options
        'birthday_options_body': '¿Qué te gustaría hacer con este cumpleaños?',
        'delete': 'Eliminar',
        'no_notes': 'Sin notas añadidas',
        'birthday_details': 'Detalles del Cumpleaños',
        
        # Toasts
        'added_toast': "'{name}' agregado",
        'deleted_toast': "'{name}' eliminado",
        
        # Preferences
        'preferences_title': 'Configuración',
        'appearance': 'Apariencia',
        'theme': 'Tema',
        'theme_description': 'Elige el tema de la aplicación',
        'color_scheme': 'Esquema de Colores',
        'color_scheme_subtitle': 'Establece el tema de apariencia de la aplicación',
        'system': 'Sistema',
        'light': 'Claro',
        'dark': 'Oscuro',
        
        # Language
        'language': 'Idioma',
        'language_description': 'Elige el idioma de la aplicación',
        'language_selection': 'Selección de Idioma',
        'language_subtitle': 'Establece el idioma de la aplicación',
        'auto': 'Automático (Sistema)',
        'turkish': 'Türkçe',
        'english': 'English',
        'spanish': 'Español',
        
        # Notifications
        'notifications': 'Notificaciones',
        'notification_settings': 'Configuración de Notificaciones',
        'notification_description': 'Configura los recordatorios de cumpleaños',
        'enable_notifications': 'Activar Notificaciones',
        'enable_notifications_subtitle': 'Recibe notificaciones de cumpleaños próximos',
        'reminder_days': 'Días de Recordatorio',
        'reminder_days_subtitle': 'Días antes del cumpleaños para enviar notificación',
        
        # About
        'about': 'Acerca de',
        'app_info': 'Información de la Aplicación',
        'version': 'Versión',
        'build_date': 'Fecha de Compilación',
        'developer': 'Desarrollador',
        'technologies': 'Tecnologías',
        'built_with': 'Construido con',
    }
}

# Current language
_current_language = 'tr'


def get_system_language():
    """Get the system language code."""
    try:
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            lang_code = system_locale.split('_')[0].lower()
            if lang_code in TRANSLATIONS:
                return lang_code
    except:
        pass
    return 'en'  # Default to English


def set_language(lang_code):
    """Set the current language."""
    global _current_language
    if lang_code == 'auto':
        _current_language = get_system_language()
    elif lang_code in TRANSLATIONS:
        _current_language = lang_code
    else:
        _current_language = 'en'


def get_language():
    """Get the current language code."""
    return _current_language


def _(key, **kwargs):
    """Get translated string for the given key."""
    text = TRANSLATIONS.get(_current_language, TRANSLATIONS['en']).get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text


def get_month_names():
    """Get list of translated month names."""
    return [
        _('january'), _('february'), _('march'), _('april'),
        _('may'), _('june'), _('july'), _('august'),
        _('september'), _('october'), _('november'), _('december')
    ]
