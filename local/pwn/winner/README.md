# Winner - Pwn 100
## Đề bài
```
Vietl0tt v1.0

nc winner.svattt.org 31335
winner.c
Binary
libc.so

Inspired by true story.
```

## Writeup
Bài này cho phép mình nhập tối đa 256 kí tự, chương trình sẽ đếm số lần xuất hiện của mỗi kí tự trong xâu mình nhập, sau đó random 4 lần lấy kí tự trong khoảng `[0-9A-Fa-f]` rồi cộng số lần xuất hiện * 1024 làm số tiền của mình. Nếu như số tiền < 0 thì chương trình sẽ in ra flag (mình đoán như thế dựa vào source code của chương trình).

Quá trình mình chọn xâu may mắn được thực hiện bởi hàm `choose`:

```c
void choose(int *n[]){
    int i;
    char c;
    printf("Please choose winning numbers [1-9a-f] (type 0 if you're done)\n");

    for(i = 0; i < 256 ; i++)
        if ( (c = getchar()) == '0' )
            break;
        else
            n[c] = (int) n[c] + 1;
}
```

Dễ dàng nhận thấy vấn đề nằm ở biến `c`, mặc dù mảng `numbers` ở hàng trên đã có len = 256, nhưng do biến `c` kiểu `char` nên có thể nhận giá trị âm được, vì vậy chúng ta có thể truy cập đến những phần tử ở ngoài mảng này. Cách giải quyết thì có nhiều cách, mình có thể suggest ví dụ như đặt `n[128+c]` hoặc dùng Pascal :evil:. Vậy từ đấy có 1 hướng, đó là chỉnh trực tiếp giá trị biến `point`.

Nhưng vấn đề là biến `point` dùng để so sánh có kiểu `unsigned int` nên khó mà có thể nhỏ hơn 0 được. Hex-Rays lúc dịch ngược còn bỏ qua luôn đoạn này, chứng tỏ là khó có thể làm theo cách này được rồi (mình cũng không dám chắc 100%, nhưng mình dám chắc đến 99% là không theo cách này được, mà biết đâu bất ngờ :sad:). Chúng ta có thể +1 tối đa 256 lần vào 1 giá trị bất kì trong khoảng 127 ô nhớ DWORD-aligned tính từ mảng `numbers` về trước, nên mình chọn cộng vào giá trị saved EIP trước khi gọi hàm `choose`. Mình sẽ nhảy vào địa chỉ lấy flag ngay sau lệnh `jnb` ở `0x08048B3E`, ở offset -31 (tương ứng với char `\xe1`), do hàm khi trả về sẽ ret về địa chỉ `0x08048A65` nên ta cần cộng giá trị saved EIP lên 217.

Flag là `SVATTT{y0u_are_true_winner_pwner_as_w3ll}`, script khai thác ở [đây](https://github.com/chitoge/SVATTT-Writeups/blob/master/pwn/winner/pwn1.py).