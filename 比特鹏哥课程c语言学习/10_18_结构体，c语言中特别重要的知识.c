#include <stdio.h>


struct stu//struct是定义结构体的关键字，x是结构体的名字。结构体就相当于python中的类。
{//打括号内的代码，就是结构体的内容 
float shen_gao;
char name[20];
int age;
float ti_zhong;
//以上这些被称为结构体的成员变量。 
 }; 
 
 //定义一个名为kkk的函数。
 void kkk(struct stu* pjsj){//函数与指针、结构体的综合应用。 
 	printf("%f %s %d %f\n",(*pjsj).shen_gao,(*pjsj).name,(*pjsj).age,(*pjsj).ti_zhong);
 	//->
 	//结构体指针变量->结构体的成员名。 
 	printf("%f %s %d %f\n",pjsj->shen_gao,pjsj->name,pjsj->age,pjsj->ti_zhong);
 } 
 
 
int main() {
	struct stu hu ={1.66,"胡成健",18,55.5};//这是在用自己创建的类型来创建一个对象。
	printf("%f %s %d %f\n",hu.shen_gao,hu.name,hu.age,hu.ti_zhong);//这不就是面象对象编程吗？对象名.属性。我相当熟悉的调用方式。
	//在c语言中，有另一种表述方式，结构体对象.成员名。 
	kkk(&hu);//用取地址符把对象s的内存地址取出，穿给kkk函数的参数，一个指针变量。 
	return 0;
} 

//比特鹏哥的前1~~24个视频，我已经看完了，也算是完整的初识了c语言。
//比特鹏哥的180个视频，是有很明确的台阶结构的，
//第一阶是1~24个视频，是初识c语言，重在全面但初步的了解c语言。
//第二阶是，25~96，是c语言的初阶内容，在初识的基础上进一步深入掌握c语言。
//第三阶段是，97~175，是c语言的进阶内容，再进一步深入的掌握c语言。 
//截止10月18日，也就是今天，我已经完成了第一阶的内容。
 
