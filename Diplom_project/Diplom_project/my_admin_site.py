from django.contrib.admin import AdminSite

class MyAdminSite(AdminSite):
    site_header = 'Управление магазином'
    site_title = 'Админ-панель'
    index_title = 'Добро пожаловать в административную панель'

my_admin_site = MyAdminSite(name='myadmin')
