#include <stdio.h>


#define ADD(X,Y) ((X)+(Y))//这是在定义一个宏，什么是宏？宏可以理解为一个一行版的函数。

//#define是定义宏的关键字。后面接宏的名字，然后是宏的参数，最后是宏体。 

int main(){
	int a=10;
	int b=20;
	int c=0;
	c=ADD(a,b);
	printf("%d",c);
	return 0;
} 
