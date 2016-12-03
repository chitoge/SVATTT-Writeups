Forensics

file: chal
md5 = cc76dd05da756250c6a7cfc123785fdd
sha1 = 8981b70c33d3c8d610823b98ad3d5a8dea016ff7

Sau khi mở file lên, ta thấy nhận ra ngay những pattern quan trọng
1. 50 4B 03 04 là HEADER của một file zip
2. 66 6C 61 67 2E 74 78 74 = flag.txt
Nhưng file zip này đã bị obfuscate với những kí tự rối, điển hình là 0D 0A.
Bằng kinh nghiệm, dễ là file này đã bị encoding bằng phương pháp [Chunked Transfer](https://en.wikipedia.org/wiki/Chunked_transfer_encoding).
Với vài dòng code, ta thiết lập lại được file zip ban đầu. Ban tổ chức đưa pass là 'svattt'. Unzip file với password này ta được flag
