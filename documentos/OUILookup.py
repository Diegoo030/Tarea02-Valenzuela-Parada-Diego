#Tarea 2-Valenzuela-Parada-Diego
import sys
import getopt
import requests
import subprocess

def print_help():
    """Imprime la ayuda del programa."""
    print("Uso: python OUILookup.py --mac <direccion_mac> | --arp | --help")
    print(" --mac: Consulta el fabricante de la MAC proporcionada.")
    print(" --arp: Muestra los fabricantes de las MACs en la tabla ARP.")
    print(" --help: Muestra este mensaje de ayuda.")

def lookup_mac(mac_address):
    """Consulta la API para obtener el fabricante de la dirección MAC."""
    url = f"https://api.maclookup.app/v2/macs/{mac_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        data = response.json()

        # Verificar si la respuesta contiene un campo 'company' o si la MAC no está en la base de datos
        if 'company' not in data or not data['company']:
            print(f"\nMAC address: {mac_address}")
            print("Fabricante: Not found")
        else:
            print(f"\nMAC address: {mac_address}")
            print(f"Fabricante: {data['company']}")
        
        print(f"Tiempo de respuesta: {response.elapsed.total_seconds() * 1000:.2f} ms")

    except requests.exceptions.HTTPError as http_err:
        # Si hay un error HTTP (por ejemplo, la API falla)
        print(f"Error en la consulta de la API: {http_err}")
    except Exception as err:
        # Otros posibles errores (conexión, formato de respuesta)
        print(f"Error: {err}")

def get_mac_vendor(mac_address):
    """Consulta el fabricante (vendor) de una dirección MAC utilizando una API."""
    url = f"https://api.maclookup.app/v2/macs/{mac_address}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        data = response.json()
        return data.get('company', 'Not found')  # Devuelve el nombre del fabricante o 'Not found' si no está disponible
    except Exception as err:
        return "Not found"

import re

def lookup_arp():
    """Consulta la tabla ARP y muestra las MACs junto con los fabricantes en el formato MAC/Vendor."""
    print("Consultando la tabla ARP...")
    print("MAC/Vendor:")
    
    try:
        # Ejecutamos el comando `arp -a` para obtener la tabla ARP.
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True, check=True)
        arp_output = result.stdout

        # Definir una expresión regular para capturar direcciones MAC válidas
        mac_regex = r"([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
        
        # Procesar el resultado para extraer las MACs
        for line in arp_output.splitlines():
            # Buscar direcciones MAC válidas en la línea
            mac_match = re.search(mac_regex, line)
            
            if mac_match:
                # Extraer la dirección MAC y darle formato consistente
                mac_address = mac_match.group(0).replace('-', ':').lower()

                # Consultar el fabricante de la MAC
                vendor = get_mac_vendor(mac_address)

                # Mostrar el resultado en formato MAC/Vendor
                print(f"{mac_address} / {vendor}")

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando arp: {e}")
    except Exception as e:
        print(f"Error procesando la tabla ARP: {e}")



def main(argv):
    """Procesa los argumentos de la línea de comandos."""
    try:
        opts, args = getopt.getopt(argv, "", ["mac=", "arp", "help"])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    if not opts:
        print_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '--help':
            print_help()
        elif opt == '--mac':
            lookup_mac(arg)
        elif opt == '--arp':
            lookup_arp()

if __name__ == "__main__":
    main(sys.argv[1:])
