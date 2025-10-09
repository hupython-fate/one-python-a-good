#include <stdio.h>

int main() {
    // 数组声明和初始化
    int numbers[5] = {10, 20, 30, 40, 50};
    /*
    int：数组元素的类型（整数）

numbers：数组名称

[5]：数组大小，表示可以存储5个整数

{10, 20, 30, 40, 50}：初始化数组的值
    */
    
    // 传统的for循环遍历数组
    for (int i = 0; i < 5; i++) {
        printf("numbers[%d] = %d\n", i, numbers[i]);
    }
    /*
    int i = 0：初始化计数器变量，从0开始

i < 5：循环条件，当i小于5时继续执行

i++：每次循环后i增加1
    */
    
    return 0;
}

