import os
import subprocess

def mostrar_codigo(ruta_script):
    """Muestra el código de un script dado."""
    ruta_script_absoluta = os.path.abspath(ruta_script)
    try:
        with open(ruta_script_absoluta, 'r') as archivo:
            codigo = archivo.read()
            print(f"\n--- Código de {ruta_script} ---\n")
            print(codigo)
            return codigo
    except FileNotFoundError:
        print("El archivo no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error al leer el archivo: {e}")
        return None

def ejecutar_codigo(ruta_script):
    """Ejecuta un script Python en una nueva terminal."""
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen(['cmd', '/k', 'python', ruta_script])
        else:  # Unix-based systems
            terminal = subprocess.Popen(['which', 'xterm'], stdout=subprocess.PIPE).communicate()[0].strip()
            if terminal:
                subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
            else:
                print("xterm no está disponible en este sistema.")
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el código: {e}")

def mostrar_menu():
    """Muestra el menú principal del programa."""
    ruta_base = os.path.dirname(os.path.abspath(__file__))

    unidades = {
        '1': 'Unidad 1',
        '2': 'Unidad 2'
    }

    while True:
        print("\nMenu Principal - Dashboard")
        for key, nombre in unidades.items():
            print(f"{key} - {nombre}")
        print("0 - Salir")

        eleccion_unidad = input("Elige una unidad o '0' para salir: ").strip()
        if eleccion_unidad == '0':
            print("Saliendo del programa.")
            break
        elif eleccion_unidad in unidades:
            ruta_unidad = os.path.join(ruta_base, unidades[eleccion_unidad])
            if os.path.exists(ruta_unidad):
                mostrar_sub_menu(ruta_unidad)
            else:
                print("La ruta de la unidad no existe.")
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

def mostrar_sub_menu(ruta_unidad):
    """Muestra el submenú para seleccionar una subcarpeta."""
    try:
        sub_carpetas = [f.name for f in os.scandir(ruta_unidad) if f.is_dir()]
        if not sub_carpetas:
            print("No hay subcarpetas disponibles.")
            return

        while True:
            print("\nSubmenú - Selecciona una subcarpeta")
            for i, carpeta in enumerate(sub_carpetas, start=1):
                print(f"{i} - {carpeta}")
            print("0 - Regresar al menú principal")

            eleccion_carpeta = input("Elige una subcarpeta o '0' para regresar: ").strip()
            if eleccion_carpeta == '0':
                break
            try:
                indice = int(eleccion_carpeta) - 1
                if 0 <= indice < len(sub_carpetas):
                    mostrar_scripts(os.path.join(ruta_unidad, sub_carpetas[indice]))
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")
    except Exception as e:
        print(f"Error al acceder a las subcarpetas: {e}")

def mostrar_scripts(ruta_sub_carpeta):
    """Muestra una lista de scripts para seleccionar y ejecutar."""
    try:
        scripts = [f.name for f in os.scandir(ruta_sub_carpeta) if f.is_file() and f.name.endswith('.py')]
        if not scripts:
            print("No hay scripts disponibles en esta subcarpeta.")
            return

        while True:
            print("\nScripts - Selecciona un script para ver y ejecutar")
            for i, script in enumerate(scripts, start=1):
                print(f"{i} - {script}")
            print("0 - Regresar al submenú anterior")

            eleccion_script = input("Elige un script o '0' para regresar: ").strip()
            if eleccion_script == '0':
                break
            try:
                indice = int(eleccion_script) - 1
                if 0 <= indice < len(scripts):
                    ruta_script = os.path.join(ruta_sub_carpeta, scripts[indice])
                    codigo = mostrar_codigo(ruta_script)
                    if codigo:
                        ejecutar = input("¿Desea ejecutar el script? (1: Sí, 0: No): ").strip()
                        if ejecutar == '1':
                            ejecutar_codigo(ruta_script)
                        elif ejecutar == '0':
                            print("No se ejecutó el script.")
                        else:
                            print("Opción no válida. Regresando al menú de scripts.")
                        input("\nPresiona Enter para volver al menú de scripts.")
                else:
                    print("Opción no válida. Por favor, intenta de nuevo.")
            except ValueError:
                print("Opción no válida. Por favor, intenta de nuevo.")
    except Exception as e:
        print(f"Error al listar los scripts: {e}")

# Ejecutar el dashboard
if __name__ == "__main__":
    mostrar_menu()
