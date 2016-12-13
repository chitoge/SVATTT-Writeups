# Tower 1
[bin](/finals/tower/tower1/bin/tower1_ada5b261ddafe3070c3b5750404ed9e14bc94513) [source](finals/tower/tower1/bin/compress.c)
hint: CRIME

##Phân tích code:
- Server lấy 1024 bytes ngớ ngẩn ở file *poc* tại */home/tower1*. Sau đó tính SHA1 của đám bytes đó rồi lưu vào biến **hash**. Ghi flag ra file "*/dev/null*" với format: 
 
>SVATTT{**hash**}

- Sau đó, server lấy một *signature* từ người dùng
- Tiếp đến, server encode base64 của poc, gọi là *b64_poc*, ghép với *signature* của mình. Ta gọi 

> data = b64_poc || 0x00 || signature || 0x00

- Cuối cùng, **do_compress**( data,len(data),hash,len(hash) )

Thử gửi một payload không có gì (''), ta được ciphertext khá dài, chi tiết xem thêm tại [đây](/finals/tower/tower1/data/data_none). Format như sau:

> ~~Header~~ + *Format* + **Offset array** + ~~Trash value~~ + **Buffer** + ~~

Nhìn vào hàm **do_compress**, ta phân tích code rõ hơn:

Block #1
```c++
    for(i = 0 ; i < in_len; i++)
        frequency[ (unsigned char) in[i] ]++; 
    for(i = 0 ; i < 256; i++)
        if(frequency[i] > frequency[max]) max = i;
    for(i = 0 ; i < key_len ; i++)
        h ^= key[i];
```
  - Tạo một bảng frequency
  - Tìm kí tự xuất hiện nhiều nhất, ghi vào biến *max*
  - Tạo key (h) = xor của các kí tự trong **hash**

Block #2
```c++
    for(i = 0; i < in_len ; i+=8){  // divide into blocks of 8
        offset = 0;
        for(n = 0; n < 8;n++){
            offset = offset << 1;
            if (in[n+i] == max) {
                offset |=  1;
            } 
            else {
                offset |=  0;
                buf[x++] = in[n+i] ^ h ;
            }
        }
        write_int8(offset);
    }
```
  - Chia data ra làm các block 8 kí tự
  - Với mỗi block
    - nếu this_block[i] không phải *max* thì xor nó với key (h), ghi vào buffer.
    - nếu this_block[i] là *max* thì giữ nguyên, ngoài ra ghi lại offset tại đó là 1, **NHƯNG** không ghi byte này vào buffer.
  - Cuối cùng với mỗi offset, convert binary thành hex. Nói cách khác, đổi 11111111 -> ff

Từ đó, ta có 3 solution, tuỳ theo mức độ *chày cối* mà chọn loại nào cũng được. Ta cùng nhau đi vào phân tích lời giải

## Solution 1
Rõ ràng là, nếu kí dự *max* không nằm trong base64 alphabet, gọi là '$', thì **b64_poc** sẽ được xor với **h** và không bị mất data nào. Phần '$' ở input nhập vào sẽ được xoá hết đi, để lại **Buffer** = **b64_poc** ^ **h**

Câu hỏi đặt ra, làm sao để tìm **h**?

Hãy nhìn vào ciphertext với trường hợp payload = ';' x 120 + '0' x 7 [tại đây](/finals/tower/tower1/data/data_out)

Nhìn vào bảng offset, ta thấy bảng có 3 số cuối là 000 -> đoạn '0' x 7 khả năng cao là đã *được* xor với **h**. Đúng thật, ahihi, mà 0 ⊕ **h** = **h** chặt rồi! Vậy nên **h** = 0xfe <(")

Vậy việc cần làm chỉ còn là giải mã **Buffer** -> **b64_poc** -> *flag* thôi!
Tham khảo code [tại đây](/finals/tower/tower1/solution1.py)

- Pros: Chỉ cần gửi 1 payload
- Cons: Cần hiểu được signature nhập vào như nào để tìm **h**

## Solution 2
Nhìn lại bảng offset, ta chỉ cần convert lại Offset array thành mã nhị phân là biết được byte nào đã bị xor với **h**. Kết hợp với kí tự *max* mà server trả về, ta biết được byte nào ở vị trí nào. Ta chỉ cần brute 65 kí tự trong base64 alphabet là có thể build lại được **b64_poc** mà không cần biết **h** là gì!
Tham khảo code [tại đây](/finals/tower/tower1/solution2.py)

- Pros: Không cần quan tâm đến **data** lẫn **h**
- Cons: Phải gửi lên server 65 lần.

## Solution 3
Câu hỏi đầu tiên đặt ra, BTC cho hint là **CRIME**. Ok, chúng ta cùng *wiki thần chưởng*: [CRIME](https://en.wikipedia.org/wiki/CRIME)

Trong link này không có gì hay đâu, chỉ có 1 cái tên duy nhất có vẻ hay ho: **Thai Duong**

Với kinh nghiệm 4 ngày ăn trưa & ngồi cạnh ảnh ở IACR-SEAMS School "Cryptography: Foundations and New Directions" ngay trước ngày thi Chung Khảo Sinh viên với An toàn thông tin, mình chả hiểu cái trang web đó nói về cái gì cả. 

Chỉ biết là CRIME Attack sẽ exploit lỗ hổng nén. Cụ tỉ là: ta sẽ control được data, bởi vì hacker biết được cả **secret cookie** ở đây là offset, và **content** ở đây là data. Khi ấy hacker có thể inject vào data rồi đối chiếu lại ở offset, làm cho các package vẫn hoạt động bình thường.

Điều này chẳng có tác dụng gì trong bài này hết vì tác giả đã encode **PoC** dưới dạng base64 làm cho alphabet của nó giảm đi đáng kể. 

Reverse Code, họ làm gì thì mình làm ngược lại thôi <(")

```python
x = 0
buf = ''
for i in range(len(offset)):
  if offset[i] == '0':
    #decode with ⊕ h
    buf += chr(ord(data[x]) ^ h)
    x += 1
  else:
    #otherwise add max to the buffer
    buf += p
```

Sau khi reverse, ta nhìn thấy được **content** ban đầu là gì, từ đó biết được *hacker* inject malicious code như nào. Bình thường, những case thực tế thì content không ngắn như thế này

Tham khảo code [tại đây](/finals/tower/tower1/solution3.py). Chắc đây là intended solution rồi các bác ạ <(")

## Patch binary
- Attemp 1: Chỉ cần duy trì HEADER & FOOTER & Ciphertext.Length. Chỉ cần patch cho đoạn 
```c++
---offset |=  1;
+++offset |=  0;
```
thế là offset trở thành 0 hết, nếu mà không có source code thì có dời mới đoán ra được data là gì. *lol*
- Attemp 2: Filter nếu signature nhập vào kí tự != base64 alphabet thì drop connection (*mình cũng chả biết làm như nào cả*)
