from des import (hoan_vi_dau, hoan_vi_cuoi, mo_rong, hoan_vi_p,
                 ham_vong, lap_lich_khoa, ma_hoa, giai_ma)

K = 0x133457799BBCDFF1
M = 0x0123456789ABCDEF
C = 0x85E813540F0AB405


def test_hoan_vi():
    assert hoan_vi_dau(M) == 0xCC00CCFFF0AAF0AA
    assert mo_rong(0xF0AAF0AA) == 0x7A15557A1555
    assert hoan_vi_p(0x5C82B597) == 0x234AA9BB
    assert hoan_vi_cuoi(0x0A4CD99543423234) == C
    assert hoan_vi_cuoi(hoan_vi_dau(M)) == M          # IP^-1(IP(x)) = x
    print('PASS: các phép hoán vị')


def test_khoa():
    khoa = lap_lich_khoa(K)
    assert khoa[0] == 0x1B02EFFC7072                  # k1
    assert khoa[1] == 0x79AED9DBC9E5                  # k2
    assert khoa[15] == 0xCB3D8B0E17F5                 # k16
    print('PASS: lập lịch khóa')


def test_ham_vong():
    k1 = lap_lich_khoa(K)[0]
    assert mo_rong(0xF0AAF0AA) ^ k1 == 0x6117BA866527
    assert ham_vong(k1, 0xF0AAF0AA) == 0x234AA9BB
    print('PASS: hàm vòng (vòng 1)')


def test_ma_hoa_giai_ma():
    assert ma_hoa(M, K) == C
    assert giai_ma(C, K) == M
    print('PASS: mã hóa và giải mã')


if __name__ == '__main__':
    test_hoan_vi()
    test_khoa()
    test_ham_vong()
    test_ma_hoa_giai_ma()