import socket
import sys

# CONFIG
HOST = "127.0.0.1" #localhost
PORT = 65432

def conectar_a_server():
	cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		cliente.connect((HOST, PORT))
		return cliente
	except ConnectionRefusedError:
		print("No se pudo conectar al servidor. Asegúrate de que el servidor esté en ejecución.")
		sys.exit(1)

def enviar_comando(cliente, command):
	print(f"Enviando comando: {command}")

	cliente.sendall(command.encode("utf-8"))
	response = cliente.recv(1024)
	return response.decode('utf-8')

def mostrar_menu():
	print("\n==== CLIENTE PYTHON ====")
	print("1. Validar nombre de usuario")
	print("2. Generar nombre de usuario")
	print("3. Generar email")
	print("4. Desconectar")
	return input("Seleccionar una opción: ")

def main():
	print("Conectando al servidor...")
	cliente = conectar_a_server()
	print("Conectado al servidor con éxito.")

	while True:
		opcion = mostrar_menu()

		if opcion == "1":
			usuario = input("Ingrese el nombre de usuario: ")
			response = enviar_comando(cliente, f"USUARIO_VALIDAR|{usuario}")
			print(f"\nRespuesta del servidor: {response}")

		elif opcion == "2":
			longitud = input("Ingrese la longitud para el nombre de usuario (5 a 20): ")
			response = enviar_comando(cliente, f"USUARIO_GENERAR|{longitud}")
			print(f"\nRespuesta del servidor: {response}")
		
		elif opcion == "3":
			usuario = input("Ingrese el nombre de usuario para generar el email: ")
			response = enviar_comando(cliente, f"EMAIL|{usuario}")
			print(f"\nRespuesta del servidor: {response}")
		
		elif opcion == "4":
			print("Desconectando del servidor...")
			enviar_comando(cliente, "DESCONECTAR")
			cliente.close()
			print("Desconexión exitosa!")
			break
		
		else:
			print("Opción no válida. Por favor intentar de nuevo")

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\nPrograma interrumpido por el usuario.")
	except Exception as e:
		print(f"Error inesperado: {e}")