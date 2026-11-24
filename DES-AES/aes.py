# AES-128 theo mục 2.2.5 (Thuật toán 2.41)

MOD = 0x11B                  # m(X) = X^8 + X^4 + X^3 + X + 1
NR = 10                      # số vòng của AES-128
RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]   # Bảng 2.15


def nhan_02(a):
    a <<= 1                  # nhân với X = dịch trái 1 bit
    if a & 0x100:            # bit bị đẩy ra bằng 1: X^8 = X^4 + X^3 + X + 1
        a ^= MOD
    return a


def nhan(a, b):
    kq = 0
    while b:
        if b & 1:
            kq ^= a          # cộng (XOR) a nhân với X^i vào kết quả
        a = nhan_02(a)
        b >>= 1
    return kq


def nghich_dao(x):
    if x == 0:
        return 0             # quy ước 0^-1 = 0
    kq = 1
    for _ in range(254):     # x^-1 = x^254 vì x^255 = 1
        kq = nhan(kq, x)
    return kq


def hop_the(x):              # y_i = u_i ^ u_{i+4} ^ u_{i+5} ^ u_{i+6} ^ u_{i+7} ^ c_i (chỉ số mod 8)
    u = nghich_dao(x)
    y = 0
    for i in range(8):
        bit = (((u >> i) & 1) ^ ((u >> ((i + 4) % 8)) & 1) ^ ((u >> ((i + 5) % 8)) & 1)
               ^ ((u >> ((i + 6) % 8)) & 1) ^ ((u >> ((i + 7) % 8)) & 1)
               ^ ((0x63 >> i) & 1))
        y |= bit << i
    return y


SBOX = [hop_the(x) for x in range(256)]
assert SBOX[0x00] == 0x63 and SBOX[0x53] == 0xED and SBOX[0x11] == 0x82
assert len(set(SBOX)) == 256                 # S là song ánh
# Trạng thái: a[r][c] = in[r + 4c] (nạp theo cột)
def nap_trang_thai(khoi):
    return [[khoi[r + 4 * c] for c in range(4)] for r in range(4)]


def doc_trang_thai(st):
    return [st[r][c] for c in range(4) for r in range(4)]


def hex_st(st):
    return ''.join('%02x' % b for b in doc_trang_thai(st))


def sub_bytes(st):
    return [[SBOX[st[r][c]] for c in range(4)] for r in range(4)]


def shift_rows(st):                          # hàng r dịch trái r vị trí
    return [[st[r][(c + r) % 4] for c in range(4)] for r in range(4)]


def mix_columns(st):
    kq = [[0] * 4 for _ in range(4)]
    for c in range(4):
        a0, a1, a2, a3 = st[0][c], st[1][c], st[2][c], st[3][c]
        kq[0][c] = nhan(2, a0) ^ nhan(3, a1) ^ a2 ^ a3
        kq[1][c] = a0 ^ nhan(2, a1) ^ nhan(3, a2) ^ a3
        kq[2][c] = a0 ^ a1 ^ nhan(2, a2) ^ nhan(3, a3)
        kq[3][c] = nhan(3, a0) ^ a1 ^ a2 ^ nhan(2, a3)
    return kq


def add_round_key(st, k):
    return [[st[r][c] ^ k[r][c] for c in range(4)] for r in range(4)]
def sub_word(w):
    return [SBOX[b] for b in w]


def rot_word(w):
    return w[1:] + w[:1]


def mo_rong_khoa(khoa):
    w = [list(khoa[4 * i: 4 * i + 4]) for i in range(4)]     # 4 từ đầu là khóa k
    for i in range(4, 4 * (NR + 1)):                          # tạo w4 ... w43
        t = w[i - 1]
        if i % 4 == 0:
            t = sub_word(rot_word(t))
            t = [t[0] ^ RCON[i // 4 - 1]] + t[1:]             # xor Rcon[i/4]
        w.append([a ^ b for a, b in zip(w[i - 4], t)])
    return w


def khoa_vong(w, i):                         # k_i gồm 4 từ w[4i..4i+3], mỗi từ là một cột
    return [[w[4 * i + c][r] for c in range(4)] for r in range(4)]    
def ma_hoa(khoi, khoa, in_ra=False):
    w = mo_rong_khoa(khoa)
    st = nap_trang_thai(khoi)
    st = add_round_key(st, khoa_vong(w, 0))
    if in_ra:
        print('Ban ro ^ k0    :', hex_st(st))
    for i in range(1, NR + 1):
        if in_ra:
            print('Vong %d' % i)
            print('  Bat dau       :', hex_st(st))
        st = sub_bytes(st)
        if in_ra:
            print('  Sau SubBytes  :', hex_st(st))
        st = shift_rows(st)
        if in_ra:
            print('  Sau ShiftRows :', hex_st(st))
        if i < NR:                           # vòng cuối bỏ MixColumns
            st = mix_columns(st)
            if in_ra:
                print('  Sau MixColumns:', hex_st(st))
        k = khoa_vong(w, i)
        if in_ra:
            print('  Khoa vong     :', hex_st(k))
        st = add_round_key(st, k)
        if in_ra:
            print('  Het vong      :', hex_st(st))
    return doc_trang_thai(st)
def hex_w(x):                                # in một từ hoặc danh sách byte
    return ''.join('%02x' % b for b in x)


def doi_chieu(ten, tinh_duoc, mong_doi):
    kq = 'KHOP' if tinh_duoc == mong_doi else 'KHONG KHOP'
    print('%-26s tinh duoc = %-34s mong doi = %-34s -> %s'
          % (ten, tinh_duoc, mong_doi, kq))


def chay(ten, ro_hex, khoa_hex):             # mã hóa đủ 10 vòng, in từng trạng thái
    print('=====', ten, '=====')
    print('Khoa   =', khoa_hex)
    print('Ban ro =', ro_hex)
    khoa = bytes.fromhex(khoa_hex)
    w = mo_rong_khoa(khoa)
    for i in range(NR + 1):
        print('k%-2d =' % i, hex_st(khoa_vong(w, i)))
    ct = hex_w(ma_hoa(bytes.fromhex(ro_hex), khoa, True))
    print('Ban ma =', ct)
    print()
    return ct


def vong_1(ten, ro_hex, khoa_hex):           # đề trên bảng: đầu ra vòng 1 và khóa con vòng 1
    print('=====', ten, '=====')
    print('Ban ro p =', ro_hex)
    print('Khoa k   =', khoa_hex)
    khoa = bytes.fromhex(khoa_hex)
    w = mo_rong_khoa(khoa)
    g = sub_word(rot_word(w[3]))
    print('--- Khoa con vong 1: w4 = w0 ^ SubWord(RotWord(w3)) ^ Rcon[1] ---')
    print('w3           =', hex_w(w[3]))
    print('RotWord(w3)  =', hex_w(rot_word(w[3])))
    print('SubWord(...) =', hex_w(g))
    print('Rcon[1]      =', '%02x000000' % RCON[0])
    g = [g[0] ^ RCON[0]] + g[1:]
    print('g(w3)        =', hex_w(g))
    for i in range(4, 8):
        print('w%d           =' % i, hex_w(w[i]))
    k1 = khoa_vong(w, 1)
    print('Khoa vong 1  =', hex_st(k1))
    print('--- Ham vong 1 ---')
    st = add_round_key(nap_trang_thai(bytes.fromhex(ro_hex)), khoa_vong(w, 0))
    print('p ^ k0        =', hex_st(st))
    st = sub_bytes(st)
    print('Sau SubBytes  =', hex_st(st))
    st = shift_rows(st)
    print('Sau ShiftRows =', hex_st(st))
    st = mix_columns(st)
    print('Sau MixColumns=', hex_st(st))
    st = add_round_key(st, k1)
    print('Dau ra vong 1 =', hex_st(st))
    print()
    return hex_st(st), hex_st(k1)


if __name__ == '__main__':
    K0 = '00' * 16
    P1 = '00' * 15 + '11'                    # ví dụ 1: một byte 0x11 (dòng đề đã chép)
    P2 = '00' * 14 + '1111'                  # ví dụ 2: hai byte 0x11 (ảnh của bạn cùng lớp)

    ra1, k1a = vong_1('VI DU 1 TREN BANG: p = 0x...0011, k = 0', P1, K0)
    ra2, k1b = vong_1('VI DU 2 TREN BANG: p = 0x...1111, k = 0', P2, K0)
    ct_c1 = chay('FIPS-197 C.1 (Vi du 2.45)',
                 '00112233445566778899aabbccddeeff', '000102030405060708090a0b0c0d0e0f')
    ct_b = chay('FIPS-197 Phu luc B',
                '3243f6a8885a308d313198a2e0370734', '2b7e151628aed2a6abf7158809cf4f3c')

    print('===== DOI CHIEU =====')
    doi_chieu('S(0x11)', '%02x' % SBOX[0x11], '82')
    doi_chieu('S(0x53) (Vi du 2.43)', '%02x' % SBOX[0x53], 'ed')
    doi_chieu('Khoa vong 1 (vi du 1)', k1a, '62636363' * 4)
    doi_chieu('Dau ra vong 1 (vi du 1)', ra1, 'e0e138d9010000000100000001000000')
    doi_chieu('Khoa vong 1 (vi du 2)', k1b, '62636363' * 4)
    doi_chieu('Dau ra vong 1 (vi du 2)', ra2, 'e0e138d9e038d9e10100000001000000')
    cot = nap_trang_thai(bytes.fromhex('6353e08c0960e104cd70b751bacad0e7'))
    doi_chieu('MixColumns (Vi du 2.44)', hex_st(mix_columns(cot)),
              '5f72641557f5bc92f7be3b291db9f91a')
    doi_chieu('Ban ma FIPS C.1', ct_c1, '69c4e0d86a7b0430d8cdb78070b4c55a')
    doi_chieu('Ban ma FIPS B', ct_b, '3925841d02dc09fbdc118597196a0b32')