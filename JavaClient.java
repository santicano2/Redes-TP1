import java.io.*;
import java.net.*;
import java.util.Scanner;

public class JavaClient {
	// CONFIG
	private static final String HOST = "127.0.0.1";
	private static final int PORT = 25565;

	private Socket socket;			// Socket de conexión TCP
	private PrintWriter out; 	 	// Stream de salida al servidor
	private BufferedReader in; 	// Stream de entrada del servidor
	private Scanner scanner; 		// Scanner para input del usuario

	public JavaClient() {
		scanner = new Scanner(System.in);
	}

	/**
	 * Establece conexión TCP con el servidor.
	 * Inicializa los streams de entrada y salida.
	 * 
	 * Si no puede conectar, termina el programa.
	*/
	public void conectarAServidor() {
		try {
			System.out.println("Conectando al servidor...");
	
			// Crea socket TCP hacia el servidor
			socket = new Socket(HOST, PORT);

			// Inicializa streams de comunicación
			out = new PrintWriter(socket.getOutputStream(), true);
			in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

			System.out.println("Conexión establecida con éxito.");
		} catch (IOException e) {
			System.out.println("No se pudo conectar al servidor: " + e.getMessage());
			System.exit(1);
		}
	}

	/**
	 * Envía un comando al servidor y recibe la respuesta.
	 * 
	 * comando Comando a enviar al servidor
	*/
	public String enviarComando(String comando) {
		try {
			System.out.println("Enviando comando: " + comando);
			out.println(comando);

			String response = in.readLine();
			System.out.println("Respuesta recibida: " + response);

			return response;
		} catch (IOException e) {
			System.out.println("Error al comunicarse con el servidor: " + e.getMessage());
			return "ERROR: " + e.getMessage();
		}
	}

	public void mostrarMenu() {
		System.out.println("\n==== CLIENTE JAVA ====");
		System.out.println("1. Generar nombre de usuario");
		System.out.println("2. Generar email");
		System.out.println("3. Desconectar");
		System.out.print("Seleccione una opción: ");
	}

	/**
	 * Función principal que maneja la interacción con el usuario.
	*/
	public void run() {
		conectarAServidor();

		boolean corriendo = true;
		while (corriendo) {
			mostrarMenu();
			String opcion = scanner.nextLine();

			try {
				switch (opcion) {
					case "1":
						// ======= GENERAR NOMBRE DE USUARIO =======
						System.out.print("Ingrese su nombre completo (nombre y apellido): ");
						String nombreCompleto = scanner.nextLine();
						String response = enviarComando("USUARIO_GENERAR|" + nombreCompleto);
						System.out.println("\nRespuesta del servidor: " + response);
						break;

					case "2":
						// ======= GENERAR EMAIL =======
						System.out.println("Generando correo electrónico basado en el nombre de usuario...");
						String emailResponse = enviarComando("EMAIL");
						System.out.println("\nRespuesta del servidor: " + emailResponse);
						break;

					case "3":
						// ======= DESCONECTAR =======
						System.out.println("Desconectando del servidor...");
						enviarComando("DESCONECTAR");
						corriendo = false;
						break;

					default:
						System.out.println("Opción no válida. Intentar de nuevo.");
						break;
				}
			} catch (Exception e) {
				System.out.println("Error en la comunicación: " + e.getMessage());
				e.printStackTrace();
				corriendo = false;
			}
		}

		cerrarConexion();
	}

	/**
	 * Cierra los streams y el socket de conexión.
	*/
	public void cerrarConexion() {
		try {		
			if (in != null) in.close();
			if (out != null) out.close();
			if (socket != null) socket.close();

			System.out.println("Desconexión exitosa!");
		} catch (IOException e) {
			System.out.println("Error al cerrar la conexión: " + e.getMessage());
		}
	}

	public static void main(String[] args) {
		JavaClient cliente = new JavaClient();

		try {
			cliente.run();
		} catch (Exception e) {
			System.out.println("Error inesperado: " + e.getMessage());
		}
	}
}