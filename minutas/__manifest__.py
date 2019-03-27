{
    'name': 'Minutas Xmarts',
    'description': 'Creación de Minutas Xmarts',
    'author': 'Pablo Osorio Gama',
    'version': '0.2',
    'depends': ['hr','project','contacts','mail','web_digital_sign'],
    'data' : [

        'security/groups_minutas.xml',
        'security/ir.model.access.csv',
        'views/minutas_view.xml',
        'reports/reporte_minuta.xml',
        'reports/reporte_orden.xml'
    ],
    'application': False,
}