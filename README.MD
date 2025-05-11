# Sistema de Sockets - Servidor y Clientes

Este repositorio contiene la implementación de un sistema de sockets compuesto por un servidor y dos clientes, desarrollados en diferentes lenguajes de programación (Python y Java).

## Requisitos

### Para el servidor y el cliente Python:

- Python 3.6 o superior

### Para el cliente Java:

- Java JDK 8 o superior
- Compilador javac

## Estructura del proyecto

```
.
├── server.py         # Servidor implementado en Python
├── python_client.py  # Cliente implementado en Python
├── JavaClient.java   # Cliente implementado en Java
└── README.md         # Este archivo
```

## Funcionalidades

El sistema implementa:

1. **Validación de nombre de usuario**:

   - Longitud entre 5 y 20 caracteres
   - Debe contener al menos una vocal
   - Debe contener al menos una consonante
   - No puede contener números

2. **Generación de nombre de usuario**:

   - Basado en la longitud especificada por el cliente (entre 5 y 20 caracteres)
   - Siempre incluye al menos una vocal y una consonante
   - No contiene números

3. **Generación de correo electrónico**:
   - Basado en el nombre de usuario
   - Dominios válidos: gmail.com y hotmail.com
   - Validación de formato correcto

## Instrucciones de ejecución

### 1. Iniciar el servidor

Abra una terminal y ejecute:

```bash
python server.py
```

Verá un mensaje indicando que el servidor está escuchando en 127.0.0.1:65432.

### 2. Ejecutar cliente Python

En una nueva terminal, ejecute:

```bash
python python_client.py
```

### 3. Compilar y ejecutar cliente Java

En una nueva terminal, compile y ejecute el cliente Java:

```bash
# Compilar
javac JavaClient.java

# Ejecutar
java JavaClient
```

## Uso del sistema

### En cualquiera de los clientes:

1. Seleccione la opción 1 para validar un nombre de usuario
2. Seleccione la opción 2 para generar un nombre de usuario basado en la longitud
3. Seleccione la opción 3 para generar una dirección de correo electrónico
4. Seleccione la opción 4 para salir

## Notas importantes

- El servidor debe estar en ejecución antes de iniciar cualquiera de los clientes
- Los clientes se conectan automáticamente al servidor en localhost (127.0.0.1)
- La comunicación se realiza a través del puerto 65432
