from des_tables import IP, E, P, PC1, PC2, SHIFTS, SBOX

MASK28 = (1 << 28) - 1
MASK32 = (1 << 32) - 1


# ---------- Thuật toán 2.37: hoán vị bit theo bảng ----------
def hoan_vi_bit(x, T, n_vao):
    y = 0
    for j in range(len(T)):
        b = (x >> (n_vao - T[j])) & 1     # bit thứ T[j] của x (đếm từ trái, bắt đầu từ 1)
        y = (y << 1) | b                  # nối b vào cuối y
    return y


# ---------- Thuật toán 2.38: các phép hoán vị và hàm vòng ----------
def lap_bang_nguoc(T):
    inv = [0] * len(T)
    for j in range(len(T)):
        inv[T[j] - 1] = j + 1             # bit j+1 của khối ra đến từ bit T[j]
    return inv


IP_INV = lap_bang_nguoc(IP)


def hoan_vi_dau(x):
    return hoan_vi_bit(x, IP, 64)


def hoan_vi_cuoi(x):
    return hoan_vi_bit(x, IP_INV, 64)


def mo_rong(R):
    return hoan_vi_bit(R, E, 32)          # 32 -> 48 bit


def hoan_vi_p(s):
    return hoan_vi_bit(s, P, 32)


def ham_vong(ki, R, in_ra=False):
    u = mo_rong(R) ^ ki                   # u = EP(R) xor k_i, 48 bit
    s = 0
    for j in range(8):
        nhom = (u >> (42 - 6 * j)) & 0x3F       # nhóm 6 bit thứ j (u_{6j+1} ... u_{6j+6})
        hang = ((nhom >> 4) & 2) | (nhom & 1)   # hàng = b1 b6
        cot = (nhom >> 1) & 0xF                 # cột = b2 b3 b4 b5
        s = (s << 4) | SBOX[j][hang][cot]       # nối 4 bit đầu ra của S_j
    f = hoan_vi_p(s)
    if in_ra:
        print('          E(R)^K = %012X  S = %08X  f = %08X' % (u, s, f))
    return f


# ---------- Thuật toán 2.39: lập lịch khóa ----------
def dich_vong_trai(x, s):
    return ((x << s) | (x >> (28 - s))) & MASK28


def lap_lich_khoa(k, in_ra=False):
    v = hoan_vi_bit(k, PC1, 64)           # 56 bit
    C = v >> 28
    D = v & MASK28
    if in_ra:
        print('C0 = %028b' % C)
        print('D0 = %028b' % D)
    khoa = []
    for i in range(16):
        C = dich_vong_trai(C, SHIFTS[i])
        D = dich_vong_trai(D, SHIFTS[i])
        ki = hoan_vi_bit((C << 28) | D, PC2, 56)
        khoa.append(ki)
        if in_ra:
            print('Vong %2d: C = %028b  D = %028b  K = %012X' % (i + 1, C, D, ki))
    return khoa


# ---------- DES = IP^-1 o sigma o rho16 o ... o rho1 o IP (công thức 2.30) ----------
def des(x, khoa, in_ra=False):
    x = hoan_vi_dau(x)
    L = x >> 32
    R = x & MASK32
    if in_ra:
        print('Sau IP: %016X' % x)
        print('L0 = %08X  R0 = %08X' % (L, R))
    for i in range(16):
        L, R = R, L ^ ham_vong(khoa[i], R, in_ra)   # rho_i: (L, R) -> (R, L xor f(k_i, R))
        if in_ra:
            print('Vong %2d: L = %08X  R = %08X' % (i + 1, L, R))
    truoc = (R << 32) | L                 # phép đổi chỗ sigma: ghép R16 || L16
    if in_ra:
        print('Truoc IP^-1 (R16 L16): %016X' % truoc)
    return hoan_vi_cuoi(truoc)


def ma_hoa(m, k, in_ra=False):
    khoa = lap_lich_khoa(k, in_ra)
    return des(m, khoa, in_ra)


def giai_ma(c, k, in_ra=False):
    khoa = lap_lich_khoa(k, in_ra)
    return des(c, khoa[::-1], in_ra)      # Mệnh đề 2.34: đảo thứ tự khóa vòng


if __name__ == '__main__':
    K = 0x133457799BBCDFF1
    M = 0x0123456789ABCDEF
    print('===== MÃ HÓA DES =====')
    print('Khóa   = %016X' % K)
    print('Bản rõ = %016X' % M)
    C = ma_hoa(M, K, True)
    print('Bản mã = %016X' % C)
    print('===== GIẢI MÃ DES =====')
    print('Giải mã = %016X' % giai_ma(C, K))