class formuta:
    def __init__(self, Param_Pp, Param_Pf, Param_Dp, Param_Ua, Param_c, Param_w, Param_q, Param_h, Param_fai):
        self.Constant_g = float(9.8)
        self.Param_Pp = float(Param_Pp)
        self.Param_Pf = float(Param_Pf)
        self.Param_Dp = float(Param_Dp)
        self.Param_Ua = float(Param_Ua)
        self.Param_c = float(Param_c)
        self.Param_w = float(Param_w)
        self.Param_q = float(Param_q)
        self.Param_h = float(Param_h)
        self.Param_fai = float(Param_fai)

    def Count(self):
        # print('qwe')
        Indirect_Param1_Vs = self.Constant_g * (self.Param_Pp - self.Param_Pf) * self.Param_Dp * self.Param_Dp / (
                18 * self.Param_Ua)
        Indirect_Param1_Fre = 466.12 * pow(self.Param_Ua, 0.57) / (
                pow(self.Param_Pf, 0.29) * pow((self.Param_Pp - self.Param_Pf), 0.29) * pow(self.Param_Dp, 0.56))
        Indirect_Param1_Fc = (1 - self.Param_c) / pow(10, self.Param_c * 1.82)
        Indirect_Param1_Fw = 0.563 * pow(self.Param_Dp / self.Param_w, 2) - 1.563 * (self.Param_Dp / self.Param_w) + 1
        # Indirect_Param1_Vc_s = Indirect_Param1_Vs * Indirect_Param1_Fre * Indirect_Param1_Fc * Indirect_Param1_Fw
        Indirect_Param1_Vc_s = Indirect_Param1_Vs * Indirect_Param1_Fc * Indirect_Param1_Fw

        # 2

        Indirect_Param2_Vfs = self.Param_q / (self.Param_w * self.Param_h)
        Param_Dp_Divide_Param_w = self.Param_Dp / self.Param_w
        print(Param_Dp_Divide_Param_w)
        if Param_Dp_Divide_Param_w <= 0.93:
            Indirect_Param2_Fh = -1.26 * pow(Param_Dp_Divide_Param_w, 2) + Param_Dp_Divide_Param_w + 0.99
        elif Param_Dp_Divide_Param_w > 0.93 and Param_Dp_Divide_Param_w <= 1:
            Indirect_Param2_Fh = -11.57 * Param_Dp_Divide_Param_w + 11.57
        Indirect_Param2_Vpx = Indirect_Param2_Vfs * Indirect_Param2_Fh

        # 3
        # Param_fai=float(input('参数:砂堤孔隙度'))
        Indirect_Param3_Rh = self.Param_w / 2
        Indirect_Param3_Uw_eq = Indirect_Param1_Vc_s / (0.041 * pow(
            (Indirect_Param1_Vc_s * self.Param_Pf * self.Param_Dp / self.Param_Ua) * pow(
                4 * Indirect_Param3_Rh / self.Param_Dp, 0.5),
            0.71))

        Indirect_Param3_Psc = (self.Param_Pf + self.Param_c * self.Param_Pp * (1 - self.Param_fai)) / (
                1 + self.Param_c * (1 - self.Param_fai))
        # Indirect_Param3_Ueq = pow(Indirect_Param3_Uw_eq / 3.46, 2) * pow(
        #     4 * self.Param_Pf * Indirect_Param3_Rh / self.Param_Ua,
        #     0.143) / (pow(self.Param_Pf / Indirect_Param3_Psc, 0.571))

        # 新加覆盖掉以前的
        Indirect_Param3_Ueq = pow(Indirect_Param3_Uw_eq / 3.46, 2) * (
                4 * Indirect_Param3_Psc * Indirect_Param3_Rh / self.Param_Ua)

        # 4
        Indirect_Param4_Heq = self.Param_h - self.Param_q / (self.Param_w * Indirect_Param3_Ueq)

        print('沉降速度', Indirect_Param1_Vc_s)
        print('水平运移速度', Indirect_Param2_Vpx)
        print('平衡流速', Indirect_Param3_Ueq)
        print('平衡高度', Indirect_Param4_Heq)

        return {
            "vcs": Indirect_Param1_Vc_s,
            "vpx": Indirect_Param2_Vpx,
            "ueq": Indirect_Param3_Ueq,
            "heq": Indirect_Param4_Heq
        }


if __name__ == '__main__':
    aasd = formuta(2850, 1020, 0.0008, 0.02, 0.3, 4.5 * 0.001, 4 / 60, 15, 0.3)

    q = aasd.Count()
    print(q)

# 压裂液的粘度为20mPa·s，砂粒密度2850kg/m3，压裂液密度为1020kg/m3，缝宽4.5mm，缝高15m，粒径0.8mm，
# 砂比为30%，排量为4m3/min，砂堤孔隙度30%。
