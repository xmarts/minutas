{
    'name': 'Minutas Xmarts',

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': 'Creación de Minutas Xmarts',

    'author': 'Xmarts',
    'website': "http://www.xmarts.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'license': 'AGPL-3',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'hr', 
        'web',
        'project', 
        'contacts', 
        'mail', 
        'web_digital_sign', 
        'hr_timesheet'
    ],
    # always loaded
    'data': [
        'security/groups_minutas.xml',
        'security/ir.model.access.csv',
        'views/project_project_view.xml',
        'views/minutas_xmarts_view.xml',
        'views/minutas_xmarts_estatus_view.xml',
        'views/minutas_xmarts_hitos_view.xml',
        'views/ubicaciones_virtuales_views.xml',
        'views/project_task_view.xml',
        'views/project_update_view.xml',
        'reports/reporte_minuta.xml',
        'reports/reporte_orden.xml',
        'wizard/account_analytic_line_wizard.xml',
    ],
    'application': False,
}
