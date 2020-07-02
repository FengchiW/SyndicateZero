import cx_Freeze

executables = [cx_Freeze.Executable("client.py", targetName="SyndicateZero.exe", icon="icon.ico")]

cx_Freeze.setup(
    name="SyndicateZero",
    version="1.3.7",
    description="Let the Syndicates Fight!",
    options={"build_exe": {"packages": ["pygame"], "include_files": "res/"}},
    executables=executables
    )