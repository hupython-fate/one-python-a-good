#include <stdio.h>
int a=12;//定义在函数之外的全局变量。 
int main(){
	int a=123;//定义在函数内部的是局部变量。
	printf("%d\n",a);//全局变量和局部变量的变量名可以是相同的。
	//输出时，局部优先。
	//不建议全局变量和局部变量的名字相同。
	//写一个代码，计算两数之和。
	int d=0;
	int c=0;
	scanf("%d%d",&d,&c);
	int smu=d+c;
	printf("%d\n",smu); 
	return 0;
}
