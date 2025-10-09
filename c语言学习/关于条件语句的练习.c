#include <stdio.h>

int main() {
    int a=2;
    int b=8;
    int s;
    s=a-b;
    if(a>b){
        printf("a与b的差值为:%d",s);
    }
    else{
        s=b-a;
        printf("a与b的差值为：%d",s);
    }
    return 0;
}