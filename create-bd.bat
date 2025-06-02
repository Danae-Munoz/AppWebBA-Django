call python manage.py runscript -v3 1-eliminar-tablas
call rmdir /s /q C:\BuenosAires\AppWebBA-Django\core\migrations
call python manage.py makemigrations
call python manage.py makemigrations core
call python manage.py migrate
call python manage.py migrate core
call python manage.py runscript -v3 2-crear-usuarios
call python manage.py runscript -v3 3-poblar-base-datos