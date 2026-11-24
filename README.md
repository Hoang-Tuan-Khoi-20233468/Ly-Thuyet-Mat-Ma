# Lý thuyết mật mã

Repo nộp bài tập môn Lý thuyết mật mã.

**Sinh viên:** Hoàng Tuấn Khôi

## Bài tập: Thiết kế thuật toán DES và AES-128

Thư mục: [`DES-AES/`](DES-AES/)

### Cấu trúc
```
DES-AES/
├── des_tables.py     # các bảng IP, EP (E), P, PC1, PC2, dãy dịch vòng, 8 hộp thế
├── des.py            # cài đặt DES (mã hóa, giải mã)
├── test_des.py       # kiểm thử bằng test vector
└── output/
    ├── des_output.txt          # kết quả chạy DES, in từng trạng thái
    └── des_test_result.txt     # kết quả chạy kiểm thử
```

### Phần DES

**Cài đặt theo** giáo trình *Mật mã và Ứng dụng: Từ cổ điển đến lượng tử* (TS. Tạ Thị Kim Huệ), mục 2.2.4:

| Nội dung trong sách | Hàm trong `des.py` |
|---|---|
| Thuật toán 2.37: hoán vị bit theo bảng | `hoan_vi_bit` |
| Thuật toán 2.38: IP, IP⁻¹, EP, P, hàm vòng | `lap_bang_nguoc`, `hoan_vi_dau`, `hoan_vi_cuoi`, `mo_rong`, `hoan_vi_p`, `ham_vong` |
| Thuật toán 2.39: lập lịch khóa | `dich_vong_trai`, `lap_lich_khoa` |
| Công thức (2.29), (2.30): 16 vòng Feistel | `des` |
| Mệnh đề 2.34: giải mã = đảo thứ tự khóa vòng | `giai_ma` |

Khối dữ liệu, khóa và các nửa C, D được biểu diễn bằng số nguyên; bảng IP⁻¹ được tính từ IP.

**Test vector** (sách, Ví dụ 2.35 đến 2.40):

| | Giá trị (hex) |
|---|---|
| Khóa | `133457799BBCDFF1` |
| Bản rõ | `0123456789ABCDEF` |
| Bản mã | `85E813540F0AB405` |

Các giá trị trung gian dùng để kiểm tra:

| Bước | Giá trị |
|---|---|
| Sau IP | `CC00CCFFF0AAF0AA` (L0 = `CC00CCFF`, R0 = `F0AAF0AA`) |
| Khóa vòng 1, 2, 16 | `1B02EFFC7072`, `79AED9DBC9E5`, `CB3D8B0E17F5` |
| Vòng 1: EP(R0) ⊕ K1 | `6117BA866527` |
| Vòng 1: đầu ra S-box, f | `5C82B597`, `234AA9BB` |
| Vòng 1: R1 | `EF4A6544` |
| Trước IP⁻¹ (R16, L16) | `0A4CD99543423234` |
| Bản mã | `85E813540F0AB405` |

### Cách chạy
```bash
cd DES-AES
python3 des.py                 # mã hóa, giải mã và in từng trạng thái
python3 test_des.py            # chạy kiểm thử, cần thấy 4 dòng PASS
```
Muốn thử khóa hoặc bản rõ khác, đổi `K` và `M` ở khối `if __name__ == '__main__'` trong `des.py`.

### Kết quả
- Output từng vòng (C, D, K, E(R)⊕K, S, f, L, R) nằm trong `DES-AES/output/des_output.txt`.
- Kết quả kiểm thử nằm trong `DES-AES/output/des_test_result.txt`.
- Mã hóa ra đúng `85E813540F0AB405` và giải mã trả về đúng `0123456789ABCDEF`.

### Phần AES-128
Đang thực hiện.