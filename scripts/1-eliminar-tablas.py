from django.db import connection
from django.conf import settings
import pyodbc


def exec_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)

def run():

    database_config = settings.DATABASES['default']
    conn_str = f"DRIVER={database_config['OPTIONS']['driver']};"
    conn_str += f"SERVER={database_config['HOST']};"
    conn_str += f"DATABASE=master;"
    conn_str += f"UID={database_config['USER']};"
    conn_str += f"PWD={database_config['PASSWORD']};"
    database = 'base_datos'
    conn = pyodbc.connect(conn_str)
    db_exists = False
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM sys.databases WHERE name = '{database}'")
        row = cursor.fetchone()
        db_exists = row[0] > 0
        cursor.execute(f"SELECT COUNT(*) FROM sys.databases WHERE name = '{database}'")
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:", e)
        db_exists = False
    finally:
        cursor.close()
        conn.close()
   
    if not db_exists:
        print('********************************************************')
        print('*                 !!!CUIDADO!!!                        *')
        print('* ANTES DE CONTINUAR SIGUE LOS SIGUIENTES PASOS:       *')
        print('* 1. ABRE MANAGEMENT STUDIO DE SQL SERVER              *')
        print('* 2. CAMBIA LA CONTRASEÑA DE "sa" POR "123"            *')
        print('* 3. VERIFICA SI EXISTE LA BD "base_datos" Y ELIMINALA *')
        print('* 4. CREA LA BD "base_datos" TOTALMENTE VACIA          *')
        print('* 5. PRESIONA <ENTER> PARA CREAR Y POBLAR LAS TABLAS   *')
        print('********************************************************')
        print()
        input('SI REALIZASTE LOS PASOS ANTERIORES PRESIONA <ENTER>: ')

    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'AUTH_USER_GROUPS') DROP TABLE AUTH_USER_GROUPS;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'AUTH_USER_USER_PERMISSIONS') DROP TABLE AUTH_USER_USER_PERMISSIONS;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'AUTH_GROUP_PERMISSIONS') DROP TABLE AUTH_GROUP_PERMISSIONS;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'AUTH_GROUP') DROP TABLE AUTH_GROUP;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'AUTH_PERMISSION') DROP TABLE AUTH_PERMISSION;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'DJANGO_ADMIN_LOG') DROP TABLE DJANGO_ADMIN_LOG;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'DJANGO_CONTENT_TYPE') DROP TABLE DJANGO_CONTENT_TYPE;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'DJANGO_MIGRATIONS') DROP TABLE DJANGO_MIGRATIONS;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'DJANGO_SESSION') DROP TABLE DJANGO_SESSION;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'AnwoStockProducto') DROP TABLE AnwoStockProducto;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'SolicitudServicio') DROP TABLE SolicitudServicio;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'GuiaDespacho') DROP TABLE GuiaDespacho;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'StockProducto') DROP TABLE StockProducto;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'Factura') DROP TABLE Factura;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'Producto') DROP TABLE Producto;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'PerfilUsuario') DROP TABLE PerfilUsuario;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'AUTHTOKEN_TOKEN') DROP TABLE AUTHTOKEN_TOKEN;")
    exec_sql("IF EXISTS (SELECT * FROM sys.tables WHERE name = 'AUTH_USER') DROP TABLE AUTH_USER;")

    
    
    
    

    
    
    