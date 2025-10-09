#include <stdio.h>


int main() {
    int my_app;
    my_app=52;
    printf("我的手机app数量是：%d",my_app);
    int my_sofa=5;
    printf("\n我的沙发数：%d",my_sofa);
    my_sofa=2;
    printf("\n后来，我的沙发数：%d",my_sofa);
    int my_kk=my_sofa;
    printf("\n我的kk数：%d",my_kk);
    my_sofa=0;
    return 0;
}