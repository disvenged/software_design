from cx_Freeze import setup, Executable

base = None

executables = [Executable("image_handling.py", base=base)]

packages = ["idna"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name="image_handling",
    options=options,
    description='All modules of Quiz converter',
    executables=executables
)
