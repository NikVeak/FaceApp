from cx_Freeze import setup, Executable


exe = Executable(
    script="main.py",
    base="Win32GUI",  # для скрытия консоли
)
setup(
    name="FaceApp",
    version="1.0",
    description="Description of your app",
    executables=[exe],
    options={
        "build_exe": {
            "include_msvcr": True,
        }
    }
)