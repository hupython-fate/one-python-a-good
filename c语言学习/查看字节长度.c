#include <stdio.h>

int main() {
    printf("int的字节长度是%zu\n",sizeof(int));
    printf("char的字节长度是%zu\n",sizeof(char));
    printf("float的字节长度是%zu\n",sizeof(float));
    printf("double的字节长度是%zu\n",sizeof(double));
    return 0;
}