#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>  // Windowsƽ̨
// #include <sys/socket.h>  // Linuxƽ̨
// #include <netinet/in.h>
// #include <arpa/inet.h>
// #include <netdb.h>

#pragma comment(lib, "ws2_32.lib")  // Windows��Ҫ��������ʱ������⡣ 

#define BUFFER_SIZE 4096
#define USER_AGENT "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"//�����ڶ��峣���� 

// ��ʼ��Winsock (Windowsƽ̨)
int init_winsock() {
    WSADATA wsa;
    return WSAStartup(MAKEWORD(2,2), &wsa);
}

// ����socket����
SOCKET create_socket(const char* host, int port) {
    struct hostent* he;
    struct sockaddr_in addr;
    
    // ����������
    if ((he = gethostbyname(host)) == NULL) {
        printf("�޷�����������: %s\n", host);
        return INVALID_SOCKET;
    }
    
    // ����socket
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        printf("����socketʧ��\n");
        return INVALID_SOCKET;
    }
    
    // ���÷�������ַ
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr = *((struct in_addr*)he->h_addr);
    
    // ���ӷ�����
    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        printf("����ʧ��\n");
        closesocket(sock);
        return INVALID_SOCKET;
    }
    
    return sock;
}

// ����HTTP GET����
int send_http_request(SOCKET sock, const char* host, const char* path) {
    char request[1024];
    
    // ����HTTP����
    snprintf(request, sizeof(request),
             "GET %s HTTP/1.1\r\n"
             "Host: %s\r\n"
             "User-Agent: %s\r\n"
             "Connection: close\r\n"
             "\r\n",
             path, host, USER_AGENT);
    
    return send(sock, request, strlen(request), 0);
}

// ����HTTP��Ӧ
void receive_response(SOCKET sock) {
    char buffer[BUFFER_SIZE];
    int bytes_received;
    FILE* output_file;
    
    // ���ļ�������
    output_file = fopen("output.html", "w");
    if (!output_file) {
        printf("�޷���������ļ�\n");
        return;
    }
    
    // ��������
    while ((bytes_received = recv(sock, buffer, BUFFER_SIZE - 1, 0)) > 0) {
        buffer[bytes_received] = '\0';
        printf("%s", buffer);  // ��ӡ������̨
        fprintf(output_file, "%s", buffer);  // ���浽�ļ�
    }
    
    fclose(output_file);
}

// �򵥵�HTML���ݽ���ʾ������ȡ�������ӣ�
void parse_links(const char* html_content) {
    const char* ptr = html_content;
    const char* link_start;
    
    printf("\n\n���ֵ�����:\n");
    
    while ((ptr = strstr(ptr, "href=\"")) != NULL) {
        ptr += 6;  // ���� href="
        link_start = ptr;
        
        // �ҵ����ӽ���������
        while (*ptr && *ptr != '"' && *ptr != '>' && *ptr != ' ') {
            ptr++;
        }
        
        // ��ӡ����
        if (ptr > link_start) {
            int len = ptr - link_start;
            char link[256];
            strncpy(link, link_start, len);
            link[len] = '\0';
            printf("- %s\n", link);
        }
    }
}

int main() {
    const char* host = "httpbin.org";  // ������վ
    const char* path = "/html";        // ����·��
    int port = 80;
    SOCKET sock;
    
    // ��ʼ��Winsock (Windows)
    if (init_winsock() != 0) {
        printf("Winsock��ʼ��ʧ��\n");
        return 1;
    }
    
    printf("��ʼ��ȡ: %s%s\n", host, path);
    
    // ����socket����
    sock = create_socket(host, port);
    if (sock == INVALID_SOCKET) {
        WSACleanup();
        return 1;
    }
    
    // ����HTTP����
    if (send_http_request(sock, host, path) <= 0) {
        printf("��������ʧ��\n");
        closesocket(sock);
        WSACleanup();
        return 1;
    }
    
    // ������Ӧ
    receive_response(sock);
    
    // ���������ӽ����߼�
    // ע�⣺ʵ��ʹ��ʱ��Ҫ�Ƚ���Ӧ���ݱ��浽������
    
    // ����
    closesocket(sock);
    WSACleanup();
    
    printf("\n��ȡ��ɣ�����ѱ��浽 output.html\n");
    
    return 0;
}
