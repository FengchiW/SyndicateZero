Hi If you're checking this out because of stackexchange THANKYOU!

As you maybe know, I was attempting to add an icon to my cx_freeze executable but whenever I do it crashes,

Note: I'm running windows 10 and using python 3.8.2

My setup.py file is as follows:

```
    import cx_Freeze
    
    executables = [cx_Freeze.Executable("client.py", targetName="SyndicateZero.exe", icon="icon.ico")]
    
    cx_Freeze.setup(
        name="SyndicateZero",
        version="1.3.7",
        description="Let the Syndicates Fight!",
        options={"build_exe": {"packages": ["pygame"], "include_files": "res/"}},
        executables=executables
        )

```

when ran from the directory the main file is located it produces:

```
    running build
    running build_exe
    copying C:\Users\Wilson\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.8_qbz5n2kfra8p0\LocalCache\local-packages\Python38\site-packages\cx_Freeze\bases\Console.exe -> build\exe.win-amd64-3.8\SyndicateZero.exe
    copying C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.8_3.8.1008.0_x64__qbz5n2kfra8p0\python38.dll -> build\exe.win-amd64-3.8\python38.dll
    error: [WinError 2] The system cannot find the file specified: 'build\\exe.win-amd64-3.8\\SyndicateZero.exe'

```

However, when running without icon="icon.ico" it is able to work without a problem