#include <cstdio>
#include <iostream>
using namespace std;

int main(){
	char s[256] = {0};
	scanf("%s",s);
	char* div; 
	div = strtok(s,"[");
	div = strtok(div,"-");
	int from = atoi(div);
	cout << from << endl;
	div = strtok(NULL,"]");
	cout << div << endl;
	return 0;
}