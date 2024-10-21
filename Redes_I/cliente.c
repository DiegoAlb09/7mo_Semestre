#include <stdio.h>
#include <string.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

#define PORT 8080
#define BUF_SIZE 1024

int main(){
  WSADATA wsaData;
  SOCKET sock;
  struct sockaddr_in server_addr;
  char buffer[BUF_SIZE] = {0};
  char message[BUF_SIZE] = {0};

  // Inicializar Winsock
  if(WSAStartup(MAKEWORD(2, 2), &wsaData) != 0){
    printf("Error al inicializar Winsock\n", WSAGetLastError());
    return 1;
  }

  // Crear socket
  if((sock = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET){
    printf("Error al crear socket\n", WSAGetLastError());
    WSACleanup();
    return 1;
  }

  // Configurar dirección del servidor
  server_addr.sin_family = AF_INET;
  server_addr.sin_port = htons(PORT);
  server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");

  // Conectar al servidor
  if(connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
    printf("Error al conectar al servidor\n", WSAGetLastError());
    closesocket(sock);
    WSACleanup();
    return 1;
  }

  // Solicitar mensaje al usuario
  printf("Ingrese un mensaje: ");
  fgets(message, BUF_SIZE, stdin);
  message[strcspn(message, "\n")] = 0; // Eliminar salto de línea

  // Enviar mensaje al servidor
  send(sock, message, strlen(message), 0);
  printf("Mensaje enviado al servidor\n");

  // Leer respuesta del servidor
  recv(sock, buffer, BUF_SIZE, 0);
  printf("Respuesta del servidor: %s\n", buffer);

  // Cerrar socket
  closesocket(sock);

  // Finalizar Winsock
  WSACleanup();

  return 0;
}