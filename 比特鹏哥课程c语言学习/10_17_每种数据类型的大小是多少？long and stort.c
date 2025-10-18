#include <stdio.h>
int main(){
	printf("%zu\n",sizeof(char));
	printf("%zu\n",sizeof(long));
	printf("%zu\n",sizeof(short));
	printf("%zu\n",sizeof(int));//c语言规定，sizeof(long)>=sizeof(int); 
	printf("%zu\n",sizeof(long long));
	printf("%zu\n",sizeof(float));
	printf("%zu\n",sizeof(double)); 
	return 0;
}//这里输出的数字的单位是字节。
 
