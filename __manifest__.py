{
    'name': 'To-Do',
    'author': 'Fo2shiria',
    'version': '17.0.0.1.0',
    'summary': 'To-Do Model First Task for me',
    'sequence': 10,
    'description': """
      To-Do App
====================
    """,
    'depends': ['base', 'contacts', 'mail', 'account', 'sale_management',
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'wizard/assign_tasks_wizard_view.xml',
        'reports/task_report.xml'
    ],
    # 'assets': {
    #     'web.assets_backend':['app_one/static/src/css/property.css']
    # },
    'application': True,
}
