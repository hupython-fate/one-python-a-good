#include <stdio.h>

void nn(){
	static int a=0;//static 修饰局部变量时，把局部变量带出了作用域。 
	//本质上，static修饰变量时，改变了变量的储存位置。
	//这影响了一个变量的生命周期。把一个局部变量的生命周期变得和程序的生命周期一样。 
	a++;
	printf("%d ",a); 
}

static int c=1000;//static修饰全局变量时，全局变量的外部链接属性会转变成内部连接属性。

//函数本身就具有外部连接属性，用static修饰函数，那么函数的外部连接属性就会变为内部链接属性。 

int main(){
	int b=0;
	while(b<10){
		nn();
		b++; 
	}
	return 0;
} 
