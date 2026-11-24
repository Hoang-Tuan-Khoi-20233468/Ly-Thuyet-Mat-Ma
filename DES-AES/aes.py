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