"""
Translations - Internationalization support for Candela.
"""

import locale

# Translation dictionaries
TRANSLATIONS = {
    'tr': {
        # Window
        'app_title': 'Candela',
        'add_event': 'Özel Gün Ekle',
        'settings': 'Ayarlar',
        
        # Empty state
        'empty_title': 'Henüz bir özel gün eklemedin, o kadar mı yalnızsın?',
        'empty_subtitle': 'Yeni bir özel gün eklemek için\n+ butonuna tıklayın',
        
        # Event list
        'upcoming_events': 'Yaklaşan Özel Günler',
        'all_events': 'Tüm Özel Günler',
        'today': 'Bugün!',
        'tomorrow': 'Yarın',
        'days_left': '{} gün kaldı',
        'was_days_ago': '{} gün önce',
        'years_old': '{} yaşına giriyor',
        'anniversary_years': '{}. yıl',
        
        # Event types
        'event_type': 'Gün Tipi',
        'birthday': 'Doğum Günü',
        'anniversary': 'Yıldönümü',
        'special_event': 'Özel Gün',
        
        # Anniversary subtypes
        'anniversary_type': 'Yıldönümü Türü',
        'wedding': 'Evlilik',
        'relationship': 'Sevgili',
        'memorial': 'Anma (Ölüm)',
        'other_anniversary': 'Diğer',
        
        # Quick add holidays
        'quick_add': 'Hazır Bayramlar',
        'new_year': 'Yılbaşı',
        'christmas': 'Noel',
        'ramadan': 'Ramazan Bayramı',
        'eid_al_adha': 'Kurban Bayramı',
        'valentines': 'Sevgililer Günü',
        'mothers_day': 'Anneler Günü',
        'fathers_day': 'Babalar Günü',
        'halloween': 'Cadılar Bayramı',
        'easter': 'Paskalya',
        'thanksgiving': 'Şükran Günü',
        
        # Event dialog
        'new_event': 'Yeni Özel Gün',
        'name': 'İsim',
        'name_placeholder': 'İsim veya açıklama girin',
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
        
        # Event options
        'event_options_body': 'Bu özel gün için ne yapmak istersiniz?',
        'delete': 'Sil',
        'no_notes': 'Not eklenmemiş',
        'event_details': 'Detaylar',
        
        # Toasts
        'added_toast': "'{name}' eklendi",
        'deleted_toast': "'{name}' silindi",
        'deleted_memorial_toast': '...',
        'deleted_love_toast': 'Her şey gönlünce olsun.',
        
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
        'notification_description': 'Özel gün hatırlatıcılarını yapılandırın',
        'enable_notifications': 'Bildirimleri Etkinleştir',
        'enable_notifications_subtitle': 'Yaklaşan özel günler için bildirim al',
        'reminder_days': 'Hatırlatma Günü',
        'reminder_days_subtitle': 'Özel günden kaç gün önce bildirim gönderilsin',
        
        # About
        'about': 'Hakkında',
        'app_info': 'Uygulama Bilgisi',
        'version': 'Sürüm',
        'build_date': 'Yapım Tarihi',
        'developer': 'Geliştirici',
        'technologies': 'Teknolojiler',
        'built_with': 'Yapılış',
        
        # Legacy support
        'add_birthday': 'Doğum Günü Ekle',
        'all_birthdays': 'Tüm Doğum Günleri',
        'new_birthday': 'Yeni Doğum Günü',
        'birthday_details': 'Doğum Günü Detayları',
        'birthday_options_body': 'Bu doğum günü için ne yapmak istersiniz?',
    },
    'en': {
        # Window
        'app_title': 'Candela',
        'add_event': 'Add Event',
        'settings': 'Settings',
        
        # Empty state
        'empty_title': "You haven't added any special days yet, are you that lonely?",
        'empty_subtitle': 'Click the + button\nto add a new special day',
        
        # Event list
        'upcoming_events': 'Upcoming Events',
        'all_events': 'All Special Days',
        'today': 'Today!',
        'tomorrow': 'Tomorrow',
        'days_left': '{} days left',
        'was_days_ago': '{} days ago',
        'years_old': 'Turning {}',
        'anniversary_years': 'Year {}',
        
        # Event types
        'event_type': 'Event Type',
        'birthday': 'Birthday',
        'anniversary': 'Anniversary',
        'special_event': 'Special Event',
        
        # Anniversary subtypes
        'anniversary_type': 'Anniversary Type',
        'wedding': 'Wedding',
        'relationship': 'Relationship',
        'memorial': 'Memorial',
        'other_anniversary': 'Other',
        
        # Quick add holidays
        'quick_add': 'Quick Add Holidays',
        'new_year': 'New Year',
        'christmas': 'Christmas',
        'ramadan': 'Eid al-Fitr (Ramadan)',
        'eid_al_adha': 'Eid al-Adha',
        'valentines': "Valentine's Day",
        'mothers_day': "Mother's Day",
        'fathers_day': "Father's Day",
        'halloween': 'Halloween',
        'easter': 'Easter',
        'thanksgiving': 'Thanksgiving',
        
        # Event dialog
        'new_event': 'New Special Day',
        'name': 'Name',
        'name_placeholder': "Enter name or description",
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
        
        # Event options
        'event_options_body': 'What would you like to do with this event?',
        'delete': 'Delete',
        'no_notes': 'No notes added',
        'event_details': 'Details',
        
        # Toasts
        'added_toast': "'{name}' added",
        'deleted_toast': "'{name}' deleted",
        'deleted_memorial_toast': '...',
        'deleted_love_toast': 'May everything go as you wish.',
        
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
        'notification_description': 'Configure event reminders',
        'enable_notifications': 'Enable Notifications',
        'enable_notifications_subtitle': 'Get notified about upcoming events',
        'reminder_days': 'Reminder Days',
        'reminder_days_subtitle': 'Days before event to send notification',
        
        # About
        'about': 'About',
        'app_info': 'Application Info',
        'version': 'Version',
        'build_date': 'Build Date',
        'developer': 'Developer',
        'technologies': 'Technologies',
        'built_with': 'Built with',
        
        # Legacy support
        'add_birthday': 'Add Birthday',
        'all_birthdays': 'All Birthdays',
        'new_birthday': 'New Birthday',
        'birthday_details': 'Birthday Details',
        'birthday_options_body': 'What would you like to do with this birthday?',
    },
    'es': {
        # Window
        'app_title': 'Candela',
        'add_event': 'Agregar Evento',
        'settings': 'Configuración',
        
        # Empty state
        'empty_title': '¿Todavía no has añadido ningún día especial, tan solo estás?',
        'empty_subtitle': 'Haz clic en el botón +\npara agregar un nuevo día especial',
        
        # Event list
        'upcoming_events': 'Próximos Eventos',
        'all_events': 'Todos los Días Especiales',
        'today': '¡Hoy!',
        'tomorrow': 'Mañana',
        'days_left': 'Faltan {} días',
        'was_days_ago': 'Hace {} días',
        'years_old': 'Cumple {}',
        'anniversary_years': 'Año {}',
        
        # Event types
        'event_type': 'Tipo de Evento',
        'birthday': 'Cumpleaños',
        'anniversary': 'Aniversario',
        'special_event': 'Evento Especial',
        
        # Anniversary subtypes
        'anniversary_type': 'Tipo de Aniversario',
        'wedding': 'Boda',
        'relationship': 'Relación',
        'memorial': 'Memorial',
        'other_anniversary': 'Otro',
        
        # Quick add holidays
        'quick_add': 'Agregar Feriados Rápido',
        'new_year': 'Año Nuevo',
        'christmas': 'Navidad',
        'ramadan': 'Eid al-Fitr (Ramadán)',
        'eid_al_adha': 'Eid al-Adha',
        'valentines': 'San Valentín',
        'mothers_day': 'Día de la Madre',
        'fathers_day': 'Día del Padre',
        'halloween': 'Halloween',
        'easter': 'Pascua',
        'thanksgiving': 'Día de Acción de Gracias',
        
        # Event dialog
        'new_event': 'Nuevo Día Especial',
        'name': 'Nombre',
        'name_placeholder': 'Ingrese nombre o descripción',
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
        
        # Event options
        'event_options_body': '¿Qué te gustaría hacer con este evento?',
        'delete': 'Eliminar',
        'no_notes': 'Sin notas añadidas',
        'event_details': 'Detalles',
        
        # Toasts
        'added_toast': "'{name}' agregado",
        'deleted_toast': "'{name}' eliminado",
        'deleted_memorial_toast': '...',
        'deleted_love_toast': 'Que todo salga como deseas.',
        
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
        'notification_description': 'Configura los recordatorios de eventos',
        'enable_notifications': 'Activar Notificaciones',
        'enable_notifications_subtitle': 'Recibe notificaciones de eventos próximos',
        'reminder_days': 'Días de Recordatorio',
        'reminder_days_subtitle': 'Días antes del evento para enviar notificación',
        
        # About
        'about': 'Acerca de',
        'app_info': 'Información de la Aplicación',
        'version': 'Versión',
        'build_date': 'Fecha de Compilación',
        'developer': 'Desarrollador',
        'technologies': 'Tecnologías',
        'built_with': 'Construido con',
        
        # Legacy support
        'add_birthday': 'Agregar Cumpleaños',
        'all_birthdays': 'Todos los Cumpleaños',
        'new_birthday': 'Nuevo Cumpleaños',
        'birthday_details': 'Detalles del Cumpleaños',
        'birthday_options_body': '¿Qué te gustaría hacer con este cumpleaños?',
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
