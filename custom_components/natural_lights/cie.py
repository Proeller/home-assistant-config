from __future__ import annotations

import logging

_LOGGER = logging.getLogger(__name__)

# Weißpunkt D65
class D65:
    GAMMA = 2.2

    XN = 0.95047
    YN = 1.00000
    ZN = 1.08883

    dn = XN + 15 * YN + 3 * ZN
    uPrimeN = (4 * XN) / dn
    vPrimeN = (9 * YN) / dn

    eps = 216.0 / 24389.0   # 0.008856
    k   = 24389.0 / 27.0    # 903.3

class XY:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"XY(X={self.x:.3f}; Y={self.y:.3f})"

class XYB(XY):
    b: int    # 0..255

    def __init__(self, xy: XY, b: int):
        self.x = xy.x
        self.y = xy.y
        self.b = b

    def __str__(self) -> str:
        return f"XYB(X={self.x:.3f}; Y={self.y:.3f}; B={self.b})"

    def To_CIELuv(self) -> CIELuv:
        Y = (self.b / 255) ** D65.GAMMA
        if self.y <= 0 or self.b <= 0:
            return CIELuv(0, 0, 0)

        # xyY -> XYZ
        X = (self.x / self.y) * Y
        Z = ((1 - self.x - self.y) / self.y) * Y

        # XYZ -> u' v'
        d = X + 15 * Y + 3 * Z
        uPrime = 0 if (d == 0) else (4 * X) / d
        vPrime = 0 if (d == 0) else (9 * Y) / d

        # L*
        yr = Y / D65.YN
        L = 116 * yr ** (1/3) - 16 if yr > D65.eps else D65.k * yr

        if L <= 0:
            return CIELuv(0, 0, 0)

        # u*, v*
        u = 13 * L * (uPrime - D65.uPrimeN)
        v = 13 * L * (vPrime - D65.vPrimeN)

        return CIELuv(L, u, v)

class CIELuv:
    L: float
    u: float
    v: float

    def __init__(self, L: float, u: float, v: float):
        self.L = L
        self.u = u
        self.v = v

    def To_xyB(self) -> XYB:
        xybZero: XYB = XYB(XY(0.0, 0.0), 0)

        if self.L <= 0:
            return xybZero

        dn = D65.XN + 15 * D65.YN + 3 * D65.ZN
        uPrimeN = (4 * D65.XN) / dn
        vPrimeN = (9 * D65.YN) / dn

        # Luv -> u'v'
        uPrime = self.u / (13 * self.L) + uPrimeN
        vPrime = self.v / (13 * self.L) + vPrimeN

        if vPrime == 0:
            return xybZero

        # L* -> Y
        Yr = ((self.L + 16) / 116.0) ** 3 if self.L > 8 else self.L / D65.k
        Y = Yr * D65.YN # Yn=1 -> Y = Yr

        # u'v'Y -> XYZ
        X = Y * (9 * uPrime) / (4 * vPrime)
        Z = Y * (12 - 3 * uPrime - 20 * vPrime) / (4 * vPrime)

        sum = X + Y + Z
        if (sum == 0):
            return xybZero

        # XYZ -> xy
        x = X / sum
        y = Y / sum

        # Y -> brightness 0..255
        briNorm = Y if D65.GAMMA == 1.0 else Y ** (1.0 / D65.GAMMA)
        bri = round(max(min(briNorm * 255.0, 255), 0))

        return XYB(XY(x, y), bri)
