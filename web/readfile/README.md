# readfile - Web 100
## Đề bài
```
http://readfile.svattt.org:8888/web100.php

http://readfile.svattt.org:8888/web100.php.bak
```
## Writeup
(credit to @mao)

Trong đề cung cấp 1 đường dẫn hợp lệ để ví dụ cơ chế hoạt động, hoặc có thể đọc hiểu sourcecode.

Để `$realsig == substr(md5($filename.$timestamp.$secretkey),0,16)`; thì cần tìm $secretkey.

Bruteforce/Dictionary Attack $secretkey để tìm tổ hợp kết hợp với filename, timestamp sao cho sig == realsig. Kết quả không tìm được $secretkey hợp lệ.

Do sử dụng "==" để so sánh giá trị => có thể bị lỗi "php type juggling"

Khi so sánh giữa "0"=="0e[a-f0-9]" sẽ có kết quả TRUE.

Bruteforce với sig=0, filename=flag.php, timestamp=[a-z0-9]{1,6}

Với timestamp=862, lấy được nội dung file flag.php

http://readfile.svattt.org:8888/web100.php?filename=flag.php&timestamp=862&sig=0

```php
<?php
echo "Where is my flag :D?";
//SVATTT{N0_m0r3_h4sh_3xtens10n_4tt4ck}
exit(0);
?>
```