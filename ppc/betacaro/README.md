# betacaro - ACM 150
## Đề bài
```
5-in-a-row and get the flag!
nc betacaro.svattt.org 19132
```

## Writeup
Bài này yêu cầu mình phải đánh cờ caro, do có timeout nên buộc phải đánh bằng script, hơn nữa yêu cầu của bài là nhập tọa độ theo một định dạng nào đấy kiểu hexstring độ dài 256. Do mình có thể lựa chọn là đi trước hoặc sau, nên anh @mao có ý tưởng làm cho 2 con bot đánh nhau, và mình là người ở giữa làm cầu nối. Đây là script của a @mao, mình chỉ sửa lại một chút cho đỡ lỗi, mặc dù vậy script vẫn còn nhiều lỗi bất ngờ :(

Flag là `SVATTT{W3lc0m3_t0_MITM!}`, script ở [đây](https://github.com/chitoge/SVATTT-Writeups/blob/master/ppc/betacaro/betacaro.py).