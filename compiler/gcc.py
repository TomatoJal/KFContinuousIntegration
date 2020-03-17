# -*- coding: UTF-8 -*-
class GCCComplier:
    """
    gcc

    -std=c99

    -DWIN_PC -DLOCAL_SOCKET -DPOLYPHASE_METER -DDLMS_TASK_ENABLE -D_CONSOLE -D_CRT_DISABLE_PERFCRIT_LOCKS
    -D_CRT_SECURE_NO_WARNINGS -DUSE_WINDOWS_OS -D__CC_WINDOWS -DPP_DC -D__LONG_LONG_SIZE__ -D__root=
    -D__no_init= -DWIN32 -DHT6x3x -D__weak= -DUSE_RTOS -DUSE_DEBUG

    "-IE:\\OnePiece\\Project\\0007.KFM\\KFMFP-01-KF92P005\\software\\source\\thirdparty\\pt-core\\lib"
    "-IE:\\OnePiece\\Project\\0007.KFM\\KFMFP-01-KF92P005\\software\\source\\thirdparty\\pt-core"
    ...

    # -O（大写的字母O），编译器对代码进行自动优化编译，输出效率更高的可执行文件
    # 数字越大，越加优化。但是通常情况下太大的优化级别可能会使生成的文件产生一系列的bug。一般可选择2；3会有一定风险。
    -O0

    # 生成调试信息。GNU 调试器可利用该信息。
    # -g: default -g1: Minimal -g3: Maximum
   -g3

    # 生成所有警告信息。
    -Wall

    # 只激活预处理,编译,和汇编,也就是他只把程序做成obj文件
    -c

    -fmessage-length=0
    # -o, 指定输出文件名
    -o "source\\app\\app2\\wan\\component\\wan_security.o"
    "..\\..\\source\\app\\app2\\wan\\component\\wan_security.c"
    """

    def __init__(self, config, gcc_path):
        """
        :param config: 配置文件
        :param gcc_path: gcc路径
        """
        self.__getattribute__(config['IDE'])(config)

    def eclipse(self, config):
        print(config)


