#include <stdio.h>

int main() {
    int yong_hu=2;
    float prise;
    prise=180;
    if(yong_hu==1){
        if(prise>100){
            printf("打95折。最终支付金额：%.2f",prise*0.95);
        }
        else {
            printf("无折扣。");
        }
    }
    else if (yong_hu==2){
        if(prise>200){
            printf("打9折。最终支付金额：%.2f",prise*0.9);
        }
        else {
            printf("打97折。最终支付金额：%.2f",prise*0.97);
        }
    }
}