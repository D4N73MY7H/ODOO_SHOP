{
    'name' : 'Hospital',
    'version' : '1.0',
    'summary': 'Hospital management',
    'author': 'admin',
    'sequence': -100,
    'description': """Hospital Module""",
    'category': 'hospital',
    'depends': ['base', 'mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizard/cancel_appointment_view.xml',
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
