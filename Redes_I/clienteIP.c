#include <stdio.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib, "Ws2_32.lib") // Para enlazar Winsock

#define PORT 28758
#define BUFFER_SIZE 1024

int main() {
    WSADATA wsaData;
    SOCKET sock;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE] = {0};
    char message[BUFFER_SIZE];

    // Inicializar Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("WSAStartup falló. Código de error: %d\n", WSAGetLastError());
        return 1;
    }

    // Crear socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET) {
        printf("Error al crear el socket. Código de error: %d\n", WSAGetLastError());
        WSACleanup();
        return 1;
    }

    // Configurar la dirección del servidor
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    
    // Reemplaza "192.168.1.10" con la dirección IP del servidor en tu red
    serv_addr.sin_addr.s_addr = inet_addr("172.16.113.86");

    // Conectar al servidor
    if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) == SOCKET_ERROR) {
        printf("Error al conectar al servidor. Código de error: %d\n", WSAGetLastError());
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    // Solicitar mensaje al usuario
    printf("Ingresa un mensaje para enviar al servidor: ");
    fgets(message, BUFFER_SIZE, stdin);
    message[strcspn(message, "\n")] = 0; // Eliminar salto de línea

    // Enviar mensaje al servidor
    send(sock, message, strlen(message), 0);
    printf("Mensaje enviado al servidor\n");

    // Leer respuesta del servidor
    recv(sock, buffer, BUFFER_SIZE, 0);
    printf("Mensaje procesado recibido del servidor: %s\n", buffer);

    // Cerrar socket
    closesocket(sock);

    // Finalizar Winsock
    WSACleanup();

    return 0;
}
