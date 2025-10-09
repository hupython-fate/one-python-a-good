#include <stdbool.h>//有了它，才能定义bool类型的变量。
#include <stdio.h>

int main() {
//条件语句的格式：如下。   
/* 
if（条件）{
    条件为真时要执行的语句
}
else{
    条件为假时要执行的语句
}
  */
// 但条件为假时，花括号内的代码内容就会被计算机跳过执行。
    bool liu_lian_shao=true; 
    if(liu_lian_shao){
        printf("我的流量很少了，请快点注意到！\n");
    } 
    //0代表着假，任何非零数字代表着真。
    //如下：
    int a=3;
    if(a){
        printf("任何非零数字代表着真。\n");
    }
    int b=3666;
    if(b>=36){
        printf("b大于等于36.");
    }
}