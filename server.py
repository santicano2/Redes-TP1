import socket
import threading
import random
import re

# CONFIG
HOST = "127.0.0.1" #localhost
PORT = 65432
DOMINIOS_VALIDOS = ["gmail.com", "hotmail.com"]
VOCALES = "aeiou"
CONSONANTES = "bcdfghjklmnñpqrstvwxyz"

def generar_usuario(tam):
	try:
		longitud = int(tam)

		if longitud < 5  or longitud > 20:
			return False, "ERROR: La longitud debe ser entre 5 y 20 caracteres"
		
		usuario = random.choice(VOCALES) + random.choice(CONSONANTES)

		longitud_restante = longitud - 2
		for _ in range(longitud_restante):
			usuario += random.choice(VOCALES + CONSONANTES)

		usuario = usuario.capitalize()

		return True, f"Nombre de usuario generado: {usuario}"
	except ValueError:
		return False, "ERROR: La longitud debe ser un número entero"

def validar_usuario(usuario):
	if len(usuario) < 5 or len(usuario) > 20:
		return False, "ERROR: El nombre de usuario debe tener entre 5 y 20 caracteres."
	
	if any(char.isdigit() for char in usuario):
		return False, "ERROR: El nombre de usuario no puede contener números."
	
	if not re.search(r'[aeiouAEIOU]', usuario):
		return False, "ERROR: el nombre de usuario debe contener al menos una vocal."
	
	if not re.search(r'[bcdfghjklmnñpqrstvwxyzBCDFGHJKLMNÑPQRSTVWXYZ]', usuario):
		return False, "ERROR: El nombre de usuario debe contener al menos una consonante."
	
	return True, "Nombre de usuario válido: " + usuario

def generar_email(usuario):

	is_valid, message = validar_usuario(usuario)
	if not is_valid:
		return False, message
	
	usuario = usuario.lower()

	dominio = random.choice(DOMINIOS_VALIDOS)

	email = f"{usuario}@{dominio}"

	return True, f"Email generado: {email}"

def manejar_cliente(conn, addr):
	print(f"[NUEVA CONEXIÓN] {addr} conectado.")

	connected = True
	while connected:
		try:
			data = conn.recv(1024).decode("utf-8")
			if not data:
				break

			data = data.strip()
			print(f"[RECIBIDO] {addr}: {data}")

			parts = data.split("|")
			command = parts[0]

			if command == "USUARIO_VALIDAR":
				is_valid, message = validar_usuario(parts[1])
				conn.sendall((message + "\n").encode('utf-8'))
				print(f"[ENVIADO] {addr}: {message}")

			elif command == "USUARIO_GENERAR":
				is_valid, message = generar_usuario(parts[1])
				conn.sendall((message + "\n").encode('utf-8'))
				print(f"[ENVIADO] {addr}: {message}")

			elif command == "EMAIL":
				is_valid, message = generar_email(parts[1])
				conn.sendall((message + "\n").encode('utf-8'))
				print(f"[ENVIADO] {addr}: {message}")
			
			elif command == "DESCONECTAR":
				connected = False
				conn.sendall(("Desconexión exitosa\n").encode('utf-8'))
				print(f"[ENVIADO] {addr}: Desconexión exitosa")

			else:
				conn.sendall(("Comando no reconocido\n").encode('utf-8'))
				print(f"[ENVIADO] {addr}: Comando no reconocido")
		
		except Exception as e:
			print(f"[ERROR] {e}")
			break
	
	print(f"[DESCONEXIÓN] {addr} desconectado.")
	conn.close()

def iniciar_servidor():
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.bind((HOST, PORT))
	server.listen()
	print(f"[INICIANDO] Servidor iniciado en {HOST}:{PORT}")

	try:
		while True:
			conn, addr = server.accept()
			thread = threading.Thread(target=manejar_cliente, args=(conn, addr))
			thread.daemon = True
			thread.start()
			print(f"[CONEXIONES ACTIVAS] {threading.active_count() - 1}")
	
	except KeyboardInterrupt:
		print("[CERRANDO] Cerrando servidor...")
	finally:
		server.close()

if __name__ == "__main__":
	print("[INICIANDO] Servidor iniciado...")
	iniciar_servidor()