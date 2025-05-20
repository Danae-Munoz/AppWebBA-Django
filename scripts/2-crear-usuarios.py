from django.contrib.auth.models import User
from datetime import datetime

def run():
    # Crear usuarios del sistema
    if not User.objects.filter(username='admin').exists():     User.objects.create_user(password='123', username='admin',     first_name='Blanca', last_name='Rojas',  email='brojas@gmail.com', is_staff=True, is_superuser=True)
    if not User.objects.filter(username='atorres').exists():   User.objects.create_user(password='123', username='atorres',   first_name='Ana',    last_name='Torres', email='atorres@duoc.cl', is_staff=False)
    if not User.objects.filter(username='jperez').exists():    User.objects.create_user(password='123', username='jperez',    first_name='Juan',   last_name='Pérez',  email='jperez@duoc.cl',  is_staff=False)
    if not User.objects.filter(username='mayala').exists():    User.objects.create_user(password='123', username='mayala',    first_name='Mario',  last_name='Ayala',  email='mayala@duoc.cl',  is_staff=False)
    if not User.objects.filter(username='jsoto').exists():     User.objects.create_user(password='123', username='jsoto',     first_name='John',   last_name='Soto',   email='jsoto@duoc.cl',   is_staff=False)
    if not User.objects.filter(username='pmora').exists():     User.objects.create_user(password='123', username='pmora',     first_name='Pedro',  last_name='Mora',   email='pmora@duoc.cl',   is_staff=False)
    if not User.objects.filter(username='jgatica').exists():   User.objects.create_user(password='123', username='jgatica',   first_name='Juan',   last_name='Gatica', email='jgatica@duoc.cl', is_staff=False)
    if not User.objects.filter(username='mvera').exists():     User.objects.create_user(password='123', username='mvera',     first_name='María',  last_name='Vera',   email='mvera@duoc.cl',   is_staff=False)
    if not User.objects.filter(username='pdiazduoc').exists(): User.objects.create_user(password='123', username='pdiazduoc', first_name='Pablo',  last_name='Díaz',   email='pdiazduoc.cl',    is_staff=False)
    if not User.objects.filter(username='creyes').exists():    User.objects.create_user(password='123', username='creyes',    first_name='Carlos', last_name='Reyes',  email='creyes@duoc.cl',  is_staff=False)
    if not User.objects.filter(username='emusk').exists():     User.objects.create_user(password='123', username='emusk',     first_name='Elon',   last_name='Musk',   email='emusk@duoc.cl',   is_staff=True)
    if not User.objects.filter(username='bgates').exists():    User.objects.create_user(password='123', username='bgates',    first_name='Bill',   last_name='Gates',  email='bgates@duoc.cl',  is_staff=True)

