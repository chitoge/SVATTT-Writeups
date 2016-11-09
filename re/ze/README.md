# ze - RE 50
## Writeup
Bài này code khá là dễ hiểu, mình xin được đưa code Hex-rays vào đây:
```C
int __cdecl main(int a1, char **a2)
{
  int result; // eax@7
  size_t v3; // [sp+14h] [bp-Ch]@3
  const char *v4; // [sp+18h] [bp-8h]@3

  if ( a1 <= 1 )
    exit(-1);
  v3 = strlen(a2[1]);
  v4 = a2[1];
  if ( v4[v3 - 1] == '\n' )
    v4[v3 - 1] = 0;
  if ( strlen(v4) != 8 )
    exit(-1);
  result = strtoul(v4, 0, 17);
  if ( result == 53 )
    result = printf("SVATTT{%s}\n", v4);
  return result;
}
```
Chương trình kiểm tra argc[1] với các điều kiện sau:
* Có độ dài bằng 8.
* Có giá trị = 53 khi xét xâu ở hệ cơ số 17.

53 (hệ 10) = 32 (hệ 17), có thể đổi bằng tay hoặc bằng script. Tuy nhiên, chương trình sử dụng hàm `strtoul()` vì vậy đối với input như `32------` hay `032xyxyz` cũng sẽ được chương trình chấp nhận, tuy vậy flag ở đây là `SVATTT{00000032}`.