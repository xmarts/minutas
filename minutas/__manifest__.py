{
    'name': 'Minutas Xmarts',
    'description': 'Creación de Minutas Xmarts',
    'author': 'Xmarts',
    'version': '14.0.2',
    'depends': ['hr','project','contacts','mail','web_digital_sign'],
    'data' : [

        'security/groups_minutas.xml',
        'security/ir.model.access.csv',
        'views/minutas_xmarts.xml',
        'views/project_project.xml',
        'views/minutas_xmarts_estatus.xml',
        'views/minutas_xmarts_hitos.xml',
        'reports/reporte_minuta.xml',
        'reports/reporte_orden.xml'
    ],
    'application': False,
}
