{
    'name' : 'Hospital',
    'version' : '1.0',
    'summary': 'Hospital management',
    'author': 'admin',
    'sequence': -100,
    'description': """Hospital Module""",
    'category': 'hospital',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/appointment_view.xml',
        'views/patient_view.xml',
        'views/menu.xml'
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {},
    'license': 'LGPL-3',
}
