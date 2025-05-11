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
			System.out.println("Respuesta recibidia: " + response);

			return response;
		} catch (IOException e) {
			System.out.println("Error al comunicarse con el servidor: " + e.getMessage());
			return "ERROR: " + e.getMessage();
		}
	}

	public void mostrarMenu() {
		System.out.println("\n==== CLIENTE JAVA ====");
		System.out.println("1. Validar nombre de usuario");
		System.out.println("2. Generar nombre de usuario");
		System.out.println("3. Generar email");
		System.out.println("4. Desconectar");
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
						System.out.print("Ingrese el nombre de usuario a validar: ");
						String usuario = scanner.nextLine();
						String response = enviarComando("USUARIO_VALIDAR|" + usuario);
						System.out.println("\nRespuesta del servidor: " + response);
						break;

					case "2":
						System.out.print("Ingrese la longitud para el nombre de usuario (5-20): ");
						String longitud = scanner.nextLine();
						String genResponse = enviarComando("USUARIO_GENERAR|" + longitud);
						System.out.println("\nRespuesta del servidor: " + genResponse);
						break;

					case "3":
						System.out.print("Ingrese su nombre de usuario para generar el email: ");
						String userEmail = scanner.nextLine();
						String emailResponse = enviarComando("EMAIL|" + userEmail);
						System.out.println("\nRespuesta del servidor: " + emailResponse);
						break;

					case "4":
						System.out.println("Desconectando del servidor...");
						enviarComando("DESCONECTAR");
						corriendo = false;
						System.out.println("Desconexión exitosa!");
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
			System.out.println("Cerrando conexiones...");
			
			if (in != null) in.close();
			if (out != null) out.close();
			if (socket != null) socket.close();

			System.out.println("Conexiones cerradas correctamente.");
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