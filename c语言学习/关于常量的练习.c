#include <stdio.h>
#include <math.h>

int main() {
    const float PI = 3.1415;
    double x;
    int ban_jing_1=2;
    int ban_jing_2=8;
    x=PI*pow(ban_jing_1,2);
    printf("半径为2的圆的面积是：%.2lf\n",x);
    x=PI*pow(ban_jing_2,2);
    printf("半径为8的圆的面积是：%.2lf\n",x);
    return 0;
}