pyinstaller --noconfirm --log-level=WARN ^
    --onefile --nowindow ^
    --add-data="README;." ^
    --add-data="image1.png;img" ^
    --add-binary="libfoo.so;lib" ^
    --hidden-import=secret1 ^
    --hidden-import=secret2 ^
    --icon=..\MLNMFLCN.ICO ^
    myscript.spec



pyinstaller -D -w --icon="C:\Users\WLH\Desktop\python\my_A\123.ico" -p C:\Users\WLH\Desktop\python\my_A A_Ui.py -n 复盘助手v1.1

pyinstaller -F -w --icon="C:\Users\WLH\Desktop\python\my_A\123.ico" -p C:\Users\WLH\Desktop\python\my_A A_Ui.py -n 复盘助手v1.1
