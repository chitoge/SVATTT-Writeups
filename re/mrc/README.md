# mrc - RE 150
## Đề bài
```
$ ./mrc flag.txt
ffc309e61f2ac3df48d3b9b64fd1720bfb95b460a1235f5d91c4f92ce90dfa516e1b8c49225b808560a9d853980662dc26984e

mrc
```

## Writeup
Bài này đọc nội dung từ file được cho qua argc[1], sau đó dùng các phép dịch và xor trên dữ liệu được nhập vào với 1 mảng hardcoded, rồi trả lại kết quả qua stdout. Bài toán hoàn toàn có thể giải được từ output quay về input, nhưng do thời gian thi có hạn (cũng một phần do mình lười nữa) nên mình brute flag luôn cho nhanh, do nhận thấy đói với xâu thử `SVATTT{` thì prefix của kết quả giống với prefix của đáp án đề đã cho.

Flag là `SVATTT{Whats_differenc3_between_my_mrc_@nd_crc}`.