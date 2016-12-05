# betacaro - ACM 150
## Đề bài
```
5-in-a-row and get the flag!
nc betacaro.svattt.org 19132
```

## Writeup
Bài này yêu cầu mình phải đánh cờ caro, do có timeout nên buộc phải đánh bằng script, hơn nữa yêu cầu của bài là nhập tọa độ theo một định dạng nào đấy kiểu hexstring độ dài 256. Do mình có thể lựa chọn là đi trước hoặc sau, nên anh @mao có ý tưởng làm cho 2 con bot đánh nhau, và mình là người ở giữa làm cầu nối. Đây là script của a @mao, mình chỉ sửa lại một chút cho đỡ lỗi, mặc dù vậy script vẫn còn nhiều lỗi bất ngờ :(

Flag là `SVATTT{W3lc0m3_t0_MITM!}`, script ở [đây](https://github.com/chitoge/SVATTT-Writeups/blob/master/ppc/betacaro/betacaro.py).

## Writeup 2
Thực ra ý tưởng cho 2 session caro đánh nhau là của @minhtt. Khi impliment, mình gặp có một số vấn đề là làm sao để fix giá trị trả về, trong khi chơi một ván caro là rất lâu. Từ đó, ngoài cách làm như trên thì mình nghĩ ra ý tưởng khác.

Mình lưu lại các giá trị server trả về và lưu thành một từ điển các bước đi với vị trí. Sau đó mình lưu 6 payload cạnh nhau rồi send dần dần cho đến khi nào thắng thì thôi. Cách này không khả thi nếu server có não. May mắn thay, server đánh random nên mình chỉ cần send đến khi nào được flag thì thôi. Well, sau vài lần chạy thì nó cũng ra được flag

p/s: bài này mình yêu cầu BTC reset server khá nhiều lần, không hiểu đây là ý tưởng của BTC cho flood server hay như nào.