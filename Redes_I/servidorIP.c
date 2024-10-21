#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <winsock2.h>

#pragma comment(lib, "Ws2_32.lib")  // Enlazar la librería Winsock

//#define PORT 8080
#define PORT 28758
#define BUFFER_SIZE 1024

// Función para convertir un string a mayúsculas y luego invertirlo
void process_message(char* message) {
    int length = strlen(message);

    // Convertir a mayúsculas
    for (int i = 0; i < length; i++) {
        message[i] = toupper(message[i]);
    }

    // Invertir el string
    for (int i = 0; i < length / 2; i++) {
        char temp = message[i];
        message[i] = message[length - i - 1];
        message[length - i - 1] = temp;
    }
}

int main() {
    WSADATA wsaData;
    SOCKET server_sock, client_sock;
    struct sockaddr_in server_addr, client_addr;
    int client_addr_size = sizeof(client_addr);
    char buffer[BUFFER_SIZE];

    // Inicializar Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("WSAStartup falló. Código de error: %d\n", WSAGetLastError());
        return 1;
    }

    // Crear socket
    if ((server_sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        printf("Error al crear el socket. Código de error: %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }

    // Configurar la dirección del servidor
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(PORT);
    server_addr.sin_addr.s_addr = INADDR_ANY;  // Escuchar en todas las interfaces

    // Enlazar el socket al puerto
    if (bind(server_sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR) {
        printf("Error al enlazar el socket. Código de error: %d\n", WSAGetLastError());
        closesocket(server_sock);
        WSACleanup();
        return 1;
    }

    // Escuchar conexiones entrantes
    if (listen(server_sock, 3) == SOCKET_ERROR) {
        printf("Error al escuchar en el puerto. Código de error: %d\n", WSAGetLastError());
        closesocket(server_sock);
        WSACleanup();
        return 1;
    }

    printf("Servidor escuchando en el puerto %d...\n", PORT);

    // Aceptar conexión del cliente
    if ((client_sock = accept(server_sock, (struct sockaddr*)&client_addr, &client_addr_size)) == INVALID_SOCKET) {
        printf("Error al aceptar conexión. Código de error: %d\n", WSAGetLastError());
        closesocket(server_sock);
        WSACleanup();
        return 1;
    }

    printf("Conexión aceptada...\n");

    // Leer el mensaje enviado por el cliente
    int valread = recv(client_sock, buffer, BUFFER_SIZE, 0);
    if (valread > 0) {
        buffer[valread] = '\0';  // Asegurar que el buffer sea una cadena válida
        printf("Mensaje recibido del cliente: %s\n", buffer);

        // Procesar el mensaje (mayúsculas y al revés)
        process_message(buffer);
        printf("Mensaje procesado: %s\n", buffer);

        // Enviar de vuelta el mensaje procesado al cliente
        send(client_sock, buffer, strlen(buffer), 0);
        printf("Mensaje enviado al cliente\n");
    }

    // Cerrar sockets
    closesocket(client_sock);
    closesocket(server_sock);

    // Finalizar Winsock
    WSACleanup();

    return 0;
}

