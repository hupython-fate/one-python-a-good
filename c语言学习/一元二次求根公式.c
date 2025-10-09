#include <stdio.h>
#include <math.h>

int main() {
    int resurt_1;
    resurt_1=2+10/8*3;
    printf("resurt_1：%d\n",resurt_1);//int类型的占位符是%d
    double resurt_2;
    resurt_2=2+10/8.0*3;
    printf("resurt_2:%lf\n",resurt_2);//double类型的占位符是%lf
    //float类型的占位符是%f
    //char类型的占位符是%c
    int a=-1;
    int b=3;
    int c=5;
    double gen;
    gen=(-b+sqrt(pow(b,2)-4*a*c))/2*a;
    double gen_2;
    gen_2=(-b-sqrt(pow(b,2)-4*a*c))/2*a;
    printf("gen:%lf和%lf",gen,gen_2);
    return 0;

}