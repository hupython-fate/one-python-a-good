#include <stdio.h>

int main() {
    int makk=89;
    int jihn=98;
    makk=jihn;
    jihn=89;
    printf("makk的成绩是：%d分",makk);
    printf("\njihn的成绩是：%d分",jihn);
}