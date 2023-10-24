import subprocess
import getopt
import sys

def cargar_archivo():
  archivo_db = "DBOUI.txt"
  datos_dict = {}
  
  with open(archivo_db, 'r', encoding='utf-8') as archivo:
    for linea in archivo:
      linea = linea.strip()
      if not linea or linea.startswith("#"):
        continue
      
      partes = linea.split("\t")
      direccion_mac = partes[0].replace("-", ":")
      fabricante = " ".join(partes[1:])
      fabricante = fabricante.strip()
      
      if fabricante.startswith("#"):
        fabricante = fabricante[1:].strip()
      datos_dict[direccion_mac] = fabricante
  return datos_dict

def obtener_datos_por_ip(ip): #Funcion Definida en el esqueleto
    datos_arp = obtener_tabla_arp()
    
    if not ip.startswith("192.168.0."):
        print("Error: IP está fuera de la red del host")
        print("No comienza con 192.168.0.")
        return

    if ip in datos_arp:
        mac = datos_arp[ip]
        mac_sin = ":".join(mac.split(":")[:3])
        
        if mac_sin in datos_archivo:
            print(f"Dirección MAC: {mac} ---- Fabricante: {datos_archivo[mac_sin]}")
        else:
            print(f"Dirección MAC: {mac} ---- Fabricante: No encontrado en BD")
    else:
        print("Error: No encontrado en la tabla ARP")

def obtener_datos_por_mac(direccion_mac): #Funcion Definida en el esqueleto

    direccion_mac_limpia = direccion_mac.upper().replace("-", ":") 
    OUI = ":".join(direccion_mac_limpia.split(":")[:3]) 
    print(OUI)
    if OUI in datos_archivo:
        return OUI, datos_archivo[OUI]
    elif direccion_mac_limpia in datos_archivo:
        return direccion_mac_limpia, datos_archivo[direccion_mac_limpia]
    else:
        return direccion_mac_limpia, "No encontrado"

def obtener_tabla_arp(): #Funcion Definida en el esqueleto
        datos_arp = {}
        tabla_arp = subprocess.check_output(['arp', '-a'], universal_newlines=True)
        
        lineas_arp = tabla_arp.split('\n')
        
        for linea in lineas_arp[2:]:
            if linea.strip():
                partes = linea.split()
                if len(partes) >= 2:
                    direccion_mac = partes[1].replace("-", ":").upper()
                    datos_arp[partes[0]] = direccion_mac
        return datos_arp

# Función para mostrar la ayuda y los ejemplos de uso
def mostrar_ayuda():
    print("Uso: python OUILookup.py --ip <IP> | --mac <IP> | --arp | [--help]")
    print("--ip : IP del host a consultar.")
    print("--mac: Dirección MAC a consultar. P.e. aa:bb:cc:00:00:00.")
    print("--arp: muestra los fabricantes de los hosts disponibles en la tabla ARP.")
    print("--help: muestra este mensaje y termina.")

def main(argv): #Funcion Definida en el esqueleto

    if len(argv) == 0:
        mostrar_ayuda()
        sys.exit()

    opciones, argumentos = getopt.getopt(argv, "i:m:ah", ["ip=", "mac=","arp","help"])

    for opcion, argumento in opciones:
        if opcion == '--help':
            mostrar_ayuda()
            sys.exit()
        elif opcion in ("-i", "--ip"):
            if argumento == '':
                sys.exit(2)
            obtener_datos_por_ip(argumento)
        elif opcion in ("-m", "--mac"):
            if argumento == '':
                sys.exit(2)
            mac, fabricante = obtener_datos_por_mac(argumento)
            print(f"Dirección MAC: {mac} ---- Fabricante: {fabricante}")
        elif opcion in ("-a", "--arp"):
            datos_arp = obtener_tabla_arp()
            print("<IP>----------------<Dirección MAC>----------------<FABRICANTE>")
            for ip in datos_arp:
                mac, fabricante = obtener_datos_por_mac(datos_arp[ip])
                print(f"{ip}\t {datos_arp[ip]}, {fabricante}")
#Variable grobal
datos_archivo = cargar_archivo()

if __name__ == "__main__":
    main(sys.argv[1:])
