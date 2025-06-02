import sys, re, os

# Validación de argumento
if len(sys.argv) != 2:
    exit("Uso: python update-db-host.py <nuevo_host_de_base_datos>")

nuevo_host = sys.argv[1]

# --- Reemplazo en settings.py ---
ruta_settings = r"C:\BuenosAires\AppWebBA-Django\AppWebBA\settings.py"
with open(ruta_settings, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Escapar barras invertidas para Django
nuevo_host_django = nuevo_host.replace("\\", "\\\\")
contenido = re.sub(r"'HOST':\s*'[^']*'", f"'HOST': '{nuevo_host_django.replace('\\', '\\\\')}'", contenido)


with open(ruta_settings, 'w', encoding='utf-8') as f:
    f.write(contenido)

# --- Reemplazo en archivos de C# ---
carpeta_bodega = r"C:\BuenosAires\BodegaBA-CSharp"
for raiz, _, archivos in os.walk(carpeta_bodega):
    for nombre in archivos:
        if nombre.lower().endswith(('.cs', '.config', '.txt')):
            ruta = os.path.join(raiz, nombre)
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()

            # Escapar caracteres especiales en el reemplazo
            nuevo_contenido = re.sub(
                r"data source=[^;]+;",
                f"data source={re.escape(nuevo_host)};",
                contenido
            )

            if contenido != nuevo_contenido:
                with open(ruta, 'w', encoding='utf-8') as f:
                    f.write(nuevo_contenido)
                print(f"Modificado: {ruta}")

print(f"\n✔ HOST actualizado a: {nuevo_host}")
