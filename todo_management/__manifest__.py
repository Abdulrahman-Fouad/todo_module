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
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
    ],
    # 'assets': {
    #     'web.assets_backend':['app_one/static/src/css/property.css']
    # },
    'application': True,
}
