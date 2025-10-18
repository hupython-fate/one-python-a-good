#include <stdio.h>
int main() {
	typedef int i;
	int a=100;
	i b=300;//注意，类型i,本质上就是对类型int的重命名。
	//也就说，变量a和变量是同一类型的。 
	printf("%d",b);
	return 0;
} 
