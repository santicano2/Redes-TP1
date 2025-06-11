import socket
import threading
import random
import re

# CONFIG
HOST = "127.0.0.1" #localhost
PORT = 25565
DOMINIOS_VALIDOS = ["gmail.com", "hotmail.com"]

# Diccionario para almacenar usuarios activos
# Clave: ip del cliente, Valor: nombre de usuario generado
usuarios_activos = {}

def procesar_nombre_completo(nombre_completo):
	"""
		Procesa un nombre completo ingresado y genera un nombre de usuario válido.

		Pasos:
			1. Verifica que el nombre completo no esté vacío.
			2. Separa el nombre completo en partes (nombre y apellidos).
			3. Remueve números de las partes.
			4. Prueba diferentes combinaciones de nombre y apellidos
			5. Verifica que la combinación tenga entre 5 y 20 caracteres, al menos 1 vocal y 1 consonante.

		Devuelve un boolean y el nombre de usuario generado en minusculas o un mensaje de error.
	"""

	partes = nombre_completo.strip().split()

	if len(partes) < 2:
		return False, "ERROR: Debe ingresar al menos nombre y apellido"
	
	# Remover numeros si hay
	partes_limpias = []
	for parte in partes:
		parte_limpia = re.sub(r'[0-9]', '', parte)
		if parte_limpia:
			partes_limpias.append(parte_limpia)

	if len(partes_limpias) < 2:
		return False, "ERROR: El nombre no puede contener numeros"
	
	# Encontrar combinacion valida
	combinaciones = [
		partes_limpias[0] + partes_limpias[1],  # nombre + primer apellido
    partes_limpias[0] + partes_limpias[-1], # nombre + ultimo apellido
    partes_limpias[0] + partes_limpias[1][:3] if len(partes_limpias[1]) > 3 else partes_limpias[0] + partes_limpias[1]  # nombre + apellido truncado
	]

	for combinacion in combinaciones:
		if 5 <= len(combinacion) <= 20:
			# Verificar vocales y consonantes
			if (re.search(r'[aeiouAEIOU]', combinacion) and 
					re.search(r'[bcdfghjklmnñpqrstvwxyzBCDFGHJKLMNÑPQRSTVWXYZ]', combinacion)):
					return True, combinacion.lower()
	
	return False, "ERROR: No se pudo generar un nombre de usuario válido con los datos proporcionados"

def generar_email(addr):
	"""
		Genera un email basado en el nombre de usuario generado previamente.

		Pasos:
			1. Verifica que el usuario ya haya generado un nombre de usuario.
			2. Selecciona un dominio aleatorio de la lista de dominios válidos.
			3. Combina el nombre de usuario con el dominio para formar el email.

		Devuelve un boolean y el email generado o un mensaje de error.
	"""

	if addr not in usuarios_activos:
		return False, "ERROR: Primero debe generar o validar un nombre de usuario."
	
	usuario = usuarios_activos[addr].lower()
	dominio = random.choice(DOMINIOS_VALIDOS)
	email = f"{usuario}@{dominio}"

	return True, f"Email generado: {email}"

def manejar_cliente(conn, addr):
	"""
		Maneja la comunicación con un cliente específico en un hilo separado.
    
    Protocolo de comunicación:
			- USUARIO_GENERAR|<nombre_completo>: Genera usuario desde nombre completo
			- EMAIL: Genera email basado en el último usuario válido
			- DESCONECTAR: Cierra la conexión
	"""

	print(f"[NUEVA CONEXIÓN] {addr} conectado.")

	connected = True
	while connected:
		try:
			data = conn.recv(1024).decode("utf-8")
			if not data:
				break

			data = data.strip()
			print(f"[RECIBIDO] {addr}: {data}")

			parts = data.split("|", 1)
			command = parts[0]

			# Generar usuario deesde nombre completo
			if command == "USUARIO_GENERAR":
				is_valid, result = procesar_nombre_completo(parts[1])
				if is_valid:
					usuarios_activos[addr] = result
					message = f"Nombre de usuario generado: {result}"
				else:
					message = result
				conn.sendall((message + "\n").encode('utf-8'))
				print(f"[ENVIADO] {addr}: {message}\n")

			elif command == "EMAIL":
				is_valid, message = generar_email(addr)
				conn.sendall((message + "\n").encode('utf-8'))
				print(f"[ENVIADO] {addr}: {message}\n")
			
			elif command == "DESCONECTAR":
				connected = False

				if addr in usuarios_activos:
					del usuarios_activos[addr]

				conn.sendall(("Desconexión exitosa\n").encode('utf-8'))
				print(f"[ENVIADO] {addr}: Desconexión exitosa\n")

			else:
				conn.sendall(("Comando no reconocido\n").encode('utf-8'))
				print(f"[ENVIADO] {addr}: Comando no reconocido\n")
		
		except Exception as e:
			print(f"[ERROR] {e}")
			break

	# Eliminar usuario al desconectar
	if addr in usuarios_activos:
		del usuarios_activos[addr]
	
	print(f"[DESCONEXIÓN] {addr} desconectado.")
	conn.close()

def iniciar_servidor():
	"""
		Función principal que inicia el servidor socket y maneja conexiones entrantes.
    
    El servidor:
			1. Crea un socket TCP
			2. Se enlaza a HOST:PORT
			3. Escucha conexiones entrantes
			4. Para cada conexión, crea un hilo separado para manejar al cliente
	"""

	# Crea socket TCP (AF_INET = IPv4, SOCK_STREAM = TCP)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Vincula el socket a la dirección y puerto especificados
	server.bind((HOST, PORT))

	# Pone el socket en modo escucha
	server.listen()
	print(f"[INICIANDO] Servidor iniciado en {HOST}:{PORT}")

	try:
		while True:
			# Acepta conexiones entrantes
			conn, addr = server.accept()

			# Crea un hilo separado para manejar este cliente
			thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
			thread.daemon = True
			thread.start()

			 # Muestra el número de conexiones activas
			print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}")
	
	except KeyboardInterrupt:
		print("[CERRANDO] Cerrando servidor...")
	finally:
		server.close()

if __name__ == "__main__":
	print("=" * 50)
	print("    SERVIDOR DE GENERACIÓN DE USUARIOS Y EMAILS")
	print("=" * 50)
	print("[INICIANDO] Servidor iniciado...")
	iniciar_servidor()