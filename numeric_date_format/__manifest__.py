{
    'name': 'Numeric Date Format',
    'version': '19.0.1.0.0',
    'summary': 'Show dates as 04/11/2026 (your language date format) instead of "Nov 4"',
    'description': """
Numeric Date Format
===================
Odoo 19 shows date fields in a short style such as "Nov 4" and hides the year
when it is the current year. This module shows every date and datetime field
in the date format set on the user's language, as Odoo 16, 17 and 18 did.
""",
    'category': 'Extra Tools',
    'author': 'TechieJuno',
    'support': 'junotechie@gmail.com',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            'numeric_date_format/static/src/**/*',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    "price": 29.0,
}
