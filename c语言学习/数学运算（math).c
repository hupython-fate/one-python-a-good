#include <stdio.h>
#include <math.h>

int main() {
    printf("9的平方根是%lf\n",sqrt(9));
    printf("2的3次方是%lf\n",pow(2,3));
    double renum=pow(9,2);
    printf("9的平方是%lf\n",renum);//使用中间变量获取计算结果。
    return 0;
}