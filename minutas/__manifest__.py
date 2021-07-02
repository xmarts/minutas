{
    'name': 'Minutas Xmarts',
    'description': 'Creación de Minutas Xmarts',
    'author': 'Xmarts',
    'version': '14.0.2',
    'depends': ['hr','project','contacts','mail','web_digital_sign'],
    'data' : [

        'security/groups_minutas.xml',
        'security/ir.model.access.csv',
        'views/minutas_xmarts_view.xml',
        'views/project_project_view.xml',
        'views/minutas_xmarts_estatus_view.xml',
        'views/minutas_xmarts_hitos_view.xml',
        'views/ubicaciones_virtuales_views.xml',
        'reports/reporte_minuta.xml',
        'reports/reporte_orden.xml'
    ],
    'application': False,
}
