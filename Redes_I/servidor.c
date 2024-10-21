#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

#define PORT 8080
#define BUF_SIZE 1024

// Función para convertir una cadena a mayúsculas e invertirla
void process_message(char *message){
  int len = strlen(message);
  for (int i = 0; i < len; i++){
    message[i] = toupper(message[i]); // Convertir a mayúsculas
  }
  // Invertir la cadena
  for (int i = 0; i < len / 2; i++){
    char temp = message[i];
    message[i] = message[len - i - 1];
    message[len - i - 1] = temp;
  }
}

int main(){
  WSADATA wsaData;
  SOCKET server_fd, new_socket;
  struct sockaddr_in server_addr, client_addr;
  int addrlen = sizeof(client_addr);
  char buffer[BUF_SIZE] = {0};

  // Inicializar Winsock
  if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0){
    printf("Error al inicializar Winsock\n", WSAGetLastError());
    return 1;
  }
  // Crear socket
  if((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == INVALID_SOCKET){
    printf("Error al crear el socket\n", WSAGetLastError());
    WSACleanup();
    return 1;
  }

  // Configurar la dirección del servidor
  server_addr.sin_family = AF_INET;
  server_addr.sin_addr.s_addr = INADDR_ANY;
  server_addr.sin_port = htons(PORT);

  // Enlazar el socket
  if (bind(server_fd, (struct sockaddr*)&server_addr, sizeof(server_addr)) == SOCKET_ERROR){
    printf("Error al enlazar. Código de error: %d\n", WSAGetLastError());
    closesocket(server_fd);
    WSACleanup();
    return 1;
  }

  // Escuchar conexiones
  if (listen(server_fd, 3) == SOCKET_ERROR){
    printf("Error al escuchar. Código de error: %d\n", WSAGetLastError());
    closesocket(server_fd);
    WSACleanup();
    return 1;
  }

  printf("Esperando conexiones...\n");

  // Aceptar conexion entrante
  if((new_socket = accept(server_fd, (struct sockaddr*)&client_addr, &addrlen)) == INVALID_SOCKET){
    printf("Error al aceptar la conexión. Código de error: %d\n", WSAGetLastError());
    closesocket(server_fd);
    WSACleanup();
    return 1;
  }

  // Leer mensaje del cliente
  recv(new_socket, buffer, BUF_SIZE, 0);
  printf("Mensaje del cliente: %s\n", buffer);

  // Procesar mensaje
  process_message(buffer);

  // Enviar mensaje al cliente
  send(new_socket, buffer, strlen(buffer), 0);
  printf("Mensaje enviado al cliente: %s\n", buffer);

  // Cerrar sockets
  closesocket(new_socket);
  closesocket(server_fd);

  // Limpiar Winsock
  WSACleanup();

  return 0;
}