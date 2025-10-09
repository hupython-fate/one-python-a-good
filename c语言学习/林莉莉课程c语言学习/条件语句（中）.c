#include <stdio.h>

int main() {
    int a=1;
    int b=2;
    if(a>b){
        printf("a大于b\n");
    }
    else if (a<b){
        printf("a小于b\n");
    }
    else{
        printf("a等于b\n");
    }
    //嵌套条件语句
    int k=365;
    int l=30;
    if(k<100){
        if(l<10){
            printf("k小于100，l小于10\n");
        }
    }
    else if(100<=k<=200){
        if(10<l<20){
            printf("k在100到200之间，l在10到20之间\n");
        }
    }
    else if(k>200){
        if(l>30){
            printf("k大于200，l大于30\n");
        }
    }
}