*********用户注意事项**********
目前该软件只支持正矩形标记的转换

note1: 
    # -F表示每次生成的exe覆盖之前的打包的exe
    # -w表示打包不包括控制台
    # --icon使用自己制作的.ico图标
    Pyinstaller -F --icon=C:/data_convert_tool/gui/pics/favicon.ico gui.py

note2:
    直接在main.exe文件下，使用cmd控制台运行main.exe, 可以看到bug
    直接在main.exe文件下，双击main.exe文件

bug1：
    打包错误bug：
    pefile modul no "PEE" #! 如果没有用到pefile模块可以卸载pefile

bug2:
    问题：hiddenimports = [sysconfig._get_sysconfigdata_name()] TypeError: _get_sysconfigdata_name() missing 1 required positional argument: 'check_exists'
    解决办法：https://cloud.tencent.com/developer/ask/212921

bug3:
    问题：双击gui.exe ImportError: OpenCV loader: missing configuration file: [‘config.py‘]. Check 
    解决办法： https://blog.csdn.net/weixin_42146296/article/details/121111744


note3: 打包资源文件
    https://blog.csdn.net/Jayden_Gu/article/details/94134409