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