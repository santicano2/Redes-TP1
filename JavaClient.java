import java.io.*;
import java.net.*;
import java.util.Scanner;

public class JavaClient {
	// CONFIG
	private static final String HOST = "127.0.0.1";
	private static final int PORT = 65432;

	private Socket socket;
	private PrintWriter out;
	private BufferedReader in;
	private Scanner scanner;

	public JavaClient() {
		scanner = new Scanner(System.in);
	}

	public void conectarAServidor() {
		try {
			System.out.println("Conectando al servidor...");
	
			socket = new Socket(HOST, PORT);
			out = new PrintWriter(socket.getOutputStream(), true);
			in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

			System.out.println("Conexión establecida con éxito.");
		} catch (IOException e) {
			System.out.println("No se pudo conectar al servidor: " + e.getMessage());
			System.exit(1);
		}
	}

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

	public void run() {
		conectarAServidor();

		boolean corriendo = true;
		while (corriendo) {
			mostrarMenu();
			String opcion = scanner.nextLine();

			try {
				switch (opcion) {
					case "1":
						System.out.print("Ingrese su nombre completo (nombre y apellido): ");
						String nombreCompleto = scanner.nextLine();
						String response = enviarComando("USUARIO_GENERAR|" + nombreCompleto);
						System.out.println("\nRespuesta del servidor: " + response);
						break;

					case "2":
						System.out.println("Generando correo electrónico basado en el nombre de usuario...");
						String emailResponse = enviarComando("EMAIL");
						System.out.println("\nRespuesta del servidor: " + emailResponse);
						break;

					case "3":
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