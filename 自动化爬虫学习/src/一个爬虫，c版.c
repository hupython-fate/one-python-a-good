#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>  // Windows平台
// #include <sys/socket.h>  // Linux平台
// #include <netinet/in.h>
// #include <arpa/inet.h>
// #include <netdb.h>

#pragma comment(lib, "ws2_32.lib")  // Windows需要。这里暂时不能理解。 

#define BUFFER_SIZE 4096
#define USER_AGENT "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"//这是在定义常量。 

// 初始化Winsock (Windows平台)
int init_winsock() {
    WSADATA wsa;
    return WSAStartup(MAKEWORD(2,2), &wsa);
}

// 创建socket连接
SOCKET create_socket(const char* host, int port) {
    struct hostent* he;
    struct sockaddr_in addr;
    
    // 解析主机名
    if ((he = gethostbyname(host)) == NULL) {
        printf("无法解析主机名: %s\n", host);
        return INVALID_SOCKET;
    }
    
    // 创建socket
    SOCKET sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock == INVALID_SOCKET) {
        printf("创建socket失败\n");
        return INVALID_SOCKET;
    }
    
    // 设置服务器地址
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr = *((struct in_addr*)he->h_addr);
    
    // 连接服务器
    if (connect(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        printf("连接失败\n");
        closesocket(sock);
        return INVALID_SOCKET;
    }
    
    return sock;
}

// 发送HTTP GET请求
int send_http_request(SOCKET sock, const char* host, const char* path) {
    char request[1024];
    
    // 构建HTTP请求
    snprintf(request, sizeof(request),
             "GET %s HTTP/1.1\r\n"
             "Host: %s\r\n"
             "User-Agent: %s\r\n"
             "Connection: close\r\n"
             "\r\n",
             path, host, USER_AGENT);
    
    return send(sock, request, strlen(request), 0);
}

// 接收HTTP响应
void receive_response(SOCKET sock) {
    char buffer[BUFFER_SIZE];
    int bytes_received;
    FILE* output_file;
    
    // 打开文件保存结果
    output_file = fopen("output.html", "w");
    if (!output_file) {
        printf("无法创建输出文件\n");
        return;
    }
    
    // 接收数据
    while ((bytes_received = recv(sock, buffer, BUFFER_SIZE - 1, 0)) > 0) {
        buffer[bytes_received] = '\0';
        printf("%s", buffer);  // 打印到控制台
        fprintf(output_file, "%s", buffer);  // 保存到文件
    }
    
    fclose(output_file);
}

// 简单的HTML内容解析示例（提取所有链接）
void parse_links(const char* html_content) {
    const char* ptr = html_content;
    const char* link_start;
    
    printf("\n\n发现的链接:\n");
    
    while ((ptr = strstr(ptr, "href=\"")) != NULL) {
        ptr += 6;  // 跳过 href="
        link_start = ptr;
        
        // 找到链接结束的引号
        while (*ptr && *ptr != '"' && *ptr != '>' && *ptr != ' ') {
            ptr++;
        }
        
        // 打印链接
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
    const char* host = "httpbin.org";  // 测试网站
    const char* path = "/html";        // 测试路径
    int port = 80;
    SOCKET sock;
    
    // 初始化Winsock (Windows)
    if (init_winsock() != 0) {
        printf("Winsock初始化失败\n");
        return 1;
    }
    
    printf("开始爬取: %s%s\n", host, path);
    
    // 创建socket连接
    sock = create_socket(host, port);
    if (sock == INVALID_SOCKET) {
        WSACleanup();
        return 1;
    }
    
    // 发送HTTP请求
    if (send_http_request(sock, host, path) <= 0) {
        printf("发送请求失败\n");
        closesocket(sock);
        WSACleanup();
        return 1;
    }
    
    // 接收响应
    receive_response(sock);
    
    // 这里可以添加解析逻辑
    // 注意：实际使用时需要先将响应内容保存到变量中
    
    // 清理
    closesocket(sock);
    WSACleanup();
    
    printf("\n爬取完成，结果已保存到 output.html\n");
    
    return 0;
}
