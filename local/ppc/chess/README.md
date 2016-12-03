# chess - PPC 250
## Đề bài
```
Dear chess masters, you have 3 rocks, can you win 2 hourses?

nc chess.svattt.org 12132
```

## Writeup
Bài này mình cũng không xem kĩ lắm, mà là do 2 đồng đội của mình là Minh và Phương xem trước. Sau đó Minh tìm ra project [sunfish](https://github.com/thomasahle/sunfish), có giao diện khá giống với bài toán được đưa ra. Từ đây mình chỉ code phần giao tiếp với server sử dụng [pwntools](), xong cho code *sunfish* đánh với server remote. Mình giảm timeout xuống còn 1 giây cho sunfish, và tốc độ còn có thể được cải thiện hơn nữa nếu sử dụng PyPy, nhưng mình thấy có ra được flag là được rồi :3

Flag là `SVATTT{Y0ur_Ch33s_G0d}`.

Script đã sửa từ sunfish ở [đây](https://github.com/chitoge/SVATTT-Writeups/blob/master/ppc/chess/sunfish_modified.py).