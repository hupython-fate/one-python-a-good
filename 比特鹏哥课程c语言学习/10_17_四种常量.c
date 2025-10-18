#include <stdio.h>
#define PA 3.14159265
//enum是一个关键字，用来定义一个枚举常量。 
enum name {
	aeil,kkkk,jjj
};
int main(){
	printf("常量有四种类型；\n");
	printf("一，是字面常量。\n");
	30;
	3.14159265;
	'A';//一个字符；
	"holle woarld!";//一个字符串。 
	//这就是一个字面常量，即不用标识符进行赋值的数字，或者字符； 
	printf("二，const修饰的常变量。\n");
	int a=10;
	a=30;//修改变量的值。
	printf("%d\n",a); 
	//在变量面前修饰const,这个值就不能被修改了。
	const float pa=3.141592;//在c语言中，被const修饰的变量本质上还是变量，但是不能被修改，已经有常量的属性。 
	//pa=12345689;//如果这一行没有被注释掉，这里会报错，因为常量不能被修改。 
	printf("%f\n",pa); 
	//如何证明被const修饰的变量本质上依旧是变量呢？
	//如下：
	//const int g=30;
	//int shu_zu[g]={0};
	//如果g是一个常量那么这个程序运行就不会报错，但如果g是一个变量，那么就会报错。 
	printf("三，#define定义的标识符常量。\n");
	printf("%lf\n",PA);//应该在main函数前使用“#define 常量名 值”的格式定义一个常量。
	int b=PA;
	printf("%d\n",b); 
	printf("四，枚举常量。\n"); 
	enum name f=aeil;//定义一个枚举常量。
	printf("%d\n",f); 
	return 0;
}
