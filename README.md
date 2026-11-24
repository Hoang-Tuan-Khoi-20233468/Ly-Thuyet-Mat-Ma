# Lý thuyết mật mã

Repo nộp bài tập môn Lý thuyết mật mã.

**Sinh viên:** Hoàng Tuấn Khôi

## Bài tập: Thiết kế thuật toán DES và AES-128

Thư mục bài làm: [`DES-AES/`](DES-AES/)

### Cấu trúc

```
DES-AES/
├── des_tables.py          # các bảng IP, EP (E), P, PC1, PC2, dãy dịch vòng, 8 hộp thế
├── des.py                 # cài đặt DES (lập lịch khóa, hàm vòng, mã hóa, giải mã)
├── aes.py                 # cài đặt AES-128 (S-box, 4 phép biến đổi, mở rộng khóa, mã hóa)
└── output/
    ├── des_output.txt     # kết quả chạy DES: in từng bước và đối chiếu với sách
    └── aes_output.txt     # kết quả chạy AES: in từng trạng thái và đối chiếu với sách
```

### Cách chạy

```bash
cd DES-AES
python3 des.py             # ghi kết quả:  python3 des.py | tee output/des_output.txt
python3 aes.py             # ghi kết quả:  python3 aes.py | tee output/aes_output.txt
```

Không cần cài thêm thư viện, chỉ cần Python 3. Cuối mỗi file output có mục `DOI CHIEU`, in giá trị chương trình tính được cạnh giá trị trong sách, mỗi dòng ghi `KHOP` hoặc `KHONG KHOP`. Đây là minh chứng chương trình chạy đúng.

---

## Phần DES

**Cài đặt theo** giáo trình *Mật mã và Ứng dụng: Từ cổ điển đến lượng tử* (TS. Tạ Thị Kim Huệ), mục 2.2.4. Khối dữ liệu, khóa và các nửa C, D được biểu diễn bằng số nguyên, hoán vị bằng các phép dịch bit. Bảng IP⁻¹ được tính từ bảng IP.

| Nội dung trong sách | Hàm trong `des.py` |
|---|---|
| Thuật toán 2.37: hoán vị bit theo bảng | `hoan_vi_bit` |
| Thuật toán 2.38: IP, IP⁻¹, EP, P, hàm vòng | `lap_bang_nguoc`, `hoan_vi_dau`, `hoan_vi_cuoi`, `mo_rong`, `hoan_vi_p`, `ham_vong` |
| Thuật toán 2.39: lập lịch khóa | `dich_vong_trai`, `lap_lich_khoa` |
| Công thức (2.29), (2.30): 16 vòng Feistel | `des` |
| Mệnh đề 2.34: giải mã là mã hóa với khóa vòng theo thứ tự ngược | `giai_ma` |

### Test vector (sách, Ví dụ 2.35 đến 2.40)

| | Giá trị (hex) |
|---|---|
| Khóa | `133457799BBCDFF1` |
| Bản rõ | `0123456789ABCDEF` |
| Bản mã | `85E813540F0AB405` |

Các giá trị trung gian được kiểm tra:

| Bước | Giá trị |
|---|---|
| Sau IP | `CC00CCFFF0AAF0AA` (L0 = `CC00CCFF`, R0 = `F0AAF0AA`) |
| Khóa vòng 1, 2, 16 | `1B02EFFC7072`, `79AED9DBC9E5`, `CB3D8B0E17F5` |
| Vòng 1: EP(R0) ⊕ k1 | `6117BA866527` |
| Vòng 1: đầu ra S-box, f(k1, R0) | `5C82B597`, `234AA9BB` |
| Vòng 1: R1 | `EF4A6544` |
| Trước IP⁻¹ (R16 ‖ L16) | `0A4CD99543423234` |
| Bản mã | `85E813540F0AB405` |

### Nội dung `output/des_output.txt`

1. **Bước 1:** lập lịch khóa: C0, D0, và C_i, D_i, k_i của 16 vòng.
2. **Bước 2:** hoán vị đầu IP, chia L0 và R0.
3. **Bước 3:** 16 vòng Feistel: với mỗi vòng in EP(R) ⊕ k_i, đầu ra S-box, f, L_i, R_i.
4. **Bước 4:** đổi chỗ R16 ‖ L16 rồi hoán vị cuối IP⁻¹, ra bản mã.
5. **Giải mã:** dùng 16 khóa vòng theo thứ tự ngược, ra lại bản rõ.
6. **Đối chiếu với sách:** 8 giá trị so với Ví dụ 2.35 đến 2.40, tất cả đều `KHOP`.

---

## Phần AES-128

**Cài đặt theo** giáo trình mục 2.2.5 (Thuật toán 2.41, công thức 2.43 đến 2.53).

| Nội dung trong sách | Hàm trong `aes.py` |
|---|---|
| Số học trong GF(2^8), m(X) = X^8 + X^4 + X^3 + X + 1 (Ví dụ 2.42) | `nhan_02`, `nhan`, `nghich_dao` |
| SubBytes: S(x) = A·x⁻¹ ⊕ c (công thức 2.43 đến 2.45) | `hop_the`, `SBOX`, `sub_bytes` |
| ShiftRows (2.46) | `shift_rows` |
| MixColumns (2.48) | `mix_columns` |
| AddRoundKey (2.50) | `add_round_key` |
| Mở rộng khóa (2.51 đến 2.53, Bảng 2.15) | `sub_word`, `rot_word`, `mo_rong_khoa`, `khoa_vong` |
| Thuật toán 2.41: mã hóa 10 vòng | `ma_hoa` |

Hộp thế S không chép bảng mà được **tính từ công thức**: lấy nghịch đảo trong GF(2^8) (lũy thừa 254) rồi áp dụng phép biến đổi affine với hằng c = `63`. Trạng thái được nạp theo cột: a[r][c] = in[r + 4c].

### Ví dụ trên bảng (khóa k = 0)

Đề: *Thực hiện các phép toán trong thuật toán AES để tìm trạng thái đầu ra của hàm vòng đầu tiên và khóa con của hàm vòng số 1.*

Chương trình chạy hai cách hiểu bản rõ p, khóa k = `0x00000000000000000000000000000000`:

| Ví dụ | Bản rõ p | Khóa con vòng 1 | Đầu ra vòng 1 |
|---|---|---|---|
| 1 | `0x00000000000000000000000000000011` (một byte 0x11) | `62636363 62636363 62636363 62636363` | `e0e138d9 01000000 01000000 01000000` |
| 2 | `0x00000000000000000000000000001111` (hai byte 0x11) | `62636363 62636363 62636363 62636363` | `e0e138d9 e038d9e1 01000000 01000000` |

Ghi chú: đề ghi p = `0x0000000000000011` (64 bit), được đệm 0 ở đầu thành 128 bit (ví dụ 1). Một số ghi chép bài giảng trong lớp có hai byte 0x11 (ví dụ 2), nên chương trình in cả hai để đối chiếu.

Các bước của hàm vòng 1 (16 byte, xếp theo cột):

| Bước | Ví dụ 1 | Ví dụ 2 |
|---|---|---|
| p ⊕ k0 | `00000000 00000000 00000000 00000011` | `00000000 00000000 00000000 00001111` |
| SubBytes | `63636363 63636363 63636363 63636382` | `63636363 63636363 63636363 63638282` |
| ShiftRows | `63636382 63636363 63636363 63636363` | `63636382 63638263 63636363 63636363` |
| MixColumns | `82825bba 63636363 63636363 63636363` | `82825bba 825bba82 63636363 63636363` |
| ⊕ khóa vòng 1 | `e0e138d9 01000000 01000000 01000000` | `e0e138d9 e038d9e1 01000000 01000000` |

Khóa con vòng 1: w3 = `00000000`, RotWord(w3) = `00000000`, SubWord = `63636363`, Rcon[1] = `01000000`, g(w3) = `62636363`, nên w4 = w5 = w6 = w7 = `62636363`.

### Test vector của sách và FIPS-197

| Khóa | Bản rõ | Bản mã |
|---|---|---|
| `000102030405060708090a0b0c0d0e0f` | `00112233445566778899aabbccddeeff` | `69c4e0d86a7b0430d8cdb78070b4c55a` |
| `2b7e151628aed2a6abf7158809cf4f3c` | `3243f6a8885a308d313198a2e0370734` | `3925841d02dc09fbdc118597196a0b32` |

Ngoài ra kiểm tra S(`53`) = `ed` (Ví dụ 2.43), S(`11`) = `82`, và MixColumns (Ví dụ 2.44): `6353e08c0960e104cd70b751bacad0e7` ra `5f72641557f5bc92f7be3b291db9f91a`.

### Nội dung `output/aes_output.txt`

1. Hai ví dụ trên bảng: tính khóa con vòng 1 (w3, RotWord, SubWord, Rcon, g(w3), w4 đến w7) và từng bước của hàm vòng 1.
2. Hai test vector của sách: 11 khóa vòng k0 đến k10 và trạng thái từng vòng (bắt đầu, sau SubBytes, ShiftRows, MixColumns, khóa vòng, hết vòng), cùng bản mã.
3. Mục `DOI CHIEU`: 9 giá trị so với sách, tất cả đều `KHOP`.

---

## Ghi chú

- Hai bài DES và AES đều tự viết theo thuật toán trong sách online, không dùng thư viện mật mã có sẵn.
- Muốn thử khóa hoặc bản rõ khác: với DES đổi `K` và `M` ở khối `if __name__ == '__main__'` trong `des.py`; với AES đổi chuỗi hex ở khối `if __name__ == '__main__'` trong `aes.py`.