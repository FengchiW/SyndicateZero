import cx_Freeze

executables = [cx_Freeze.Executable("newclient.py")]

cx_Freeze.setup(
    name="SyndicateZero",
    version="0.1",
    description="Let the Syndicates Fight!",
    options={"build_exe": {"packages": ["pygame"]}},
    executables=executables

    )