#include <stdio.h>

int main() {
    int int_1=80;
    printf("int_1:%d",int_1);
    char char_1='A';
    printf("\nchar_1:%c,对应的ASCII编码为%d.",char_1,char_1);
    char char_2;
    char_2=int_1;
    printf("\nchar_2:%c.",char_2);
    printf("\nchar类型所占用的字节数为：%zu",sizeof(char));
    return 0;
}