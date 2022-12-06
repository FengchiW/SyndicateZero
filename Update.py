# This file is used to update the git repository
import json
import os
import datetime


def main():
    # read the package.json file
    with open("package.json", "r") as f:
        currentData = json.load(f)

        # parse version Major.Minor.Patch.Build
        version = currentData["version"].split(".")
        major = int(version[0])
        minor = int(version[1])
        patch = int(version[2])
        build = int(version[3])

        isMinorUpdate = input("Is this a minor update? (y/n): ")
        if isMinorUpdate == "y":
            minor += 1
            patch = 0
        else:
            patch += 1

        shouldUpdateRemote = input("Should the remote be updated? (y/n): ")
        if shouldUpdateRemote == "y":
            shouldUpdateRemote = True
        else:
            shouldUpdateRemote = False

        shouldDoBuild = 'n'
        if isMinorUpdate == "y":
            shouldDoBuild = "y"
        else:
            shouldDoBuild = input("Should a build be made? (y/n): ")
        if shouldDoBuild == "y":
            nuitkaFlags = ["--onefile",
                           "--output-dir=build",
                           "--windows-disable-console",
                           "--windows-icon-from-ico=res/icon.ico"]
            flagsStr = " ".join(nuitkaFlags)
            os.system(f"python -m nuitka {flagsStr} main.py")
            # check if build/prod exists
            if not os.path.exists("build/prod"):
                os.makedirs("build/prod")
            # move the build to build/prod
            os.system("mv build/main.exe build/prod")
            # copy the resources to build/prod
            os.system("cp -r res build/prod")
            # zip resources and executable
            build += 1
            versionAsString = f"{major}.{minor}.{patch}.{build}"
            zipName = f"build/SZ-{versionAsString}.zip"
            execPath = "build/prod/main.exe"
            resPath = "build/prod/res"
            os.system(
                f"zip -r {zipName} {execPath} {resPath}")

        versionAsString = f"{major}.{minor}.{patch}.{build}"
        currentData["version"] = versionAsString
        changeMessage = ""

        addedChanges: list[str] = []
        addedChange = input("Added changes (d/Done to finish): ")
        while (addedChange != "d" and addedChange != "D"
               and addedChange != "done" and addedChange != "Done"):
            addedChanges.append(addedChange)
            addedChange = input("Added changes (d/Done to finish): ")

        changedChanges: list[str] = []
        changedChange = input("Changed changes (d/Done to finish): ")
        while (changedChange != "d" and changedChange != "D"
                and changedChange != "done" and changedChange != "Done"):
            changedChanges.append(changedChange)
            changedChange = input("Changed changes (d/Done to finish): ")

        fixedChanges: list[str] = []
        fixedChange = input("Fixed changes (d/Done to finish): ")
        while (fixedChange != "d" and fixedChange != "D"
                and fixedChange != "done" and fixedChange != "Done"):
            fixedChanges.append(fixedChange)
            fixedChange = input("Fixed changes (d/Done to finish): ")

        removedChanges: list[str] = []
        removedChange = input("Removed changes (d/Done to finish): ")
        while (removedChange != "d" and removedChange != "D"
                and removedChange != "done" and removedChange != "Done"):
            removedChanges.append(removedChange)
            removedChange = input("Removed changes (d/Done to finish): ")

        # current date
        now = datetime.datetime.now()
        currentData["lastChange"] = now.strftime("%Y-%m-%d")

        # write the changes to the changelog
        with open("CHANGELOG.md", "a") as f:
            # append change to end
            f.write(
                f"\n\n## [{versionAsString}] - {currentData['lastChange']}\n")

            if (len(addedChanges) > 0):
                f.write("### Added\n")
                for change in addedChanges:
                    f.write(f"  - {change}\n")

            if (len(changedChanges) > 0):
                f.write("### Changed\n")
                for change in changedChanges:
                    f.write(f"  - {change}\n")

            if (len(fixedChanges) > 0):
                f.write("### Fixed\n")
                for change in fixedChanges:
                    f.write(f"  - {change}\n")

            if (len(removedChanges) > 0):
                f.write("### Removed\n")
                for change in removedChanges:
                    f.write(f"  - {change}\n")

        # write the new version to the package.json file
        with open("package.json", "w") as f:
            json.dump(currentData, f, indent=2)

        if shouldUpdateRemote:
            changeMessage = f"v{versionAsString} - {currentData['lastChange']}"
            os.system("git add .")
            os.system(f"git commit -m \"{changeMessage}\"")
            os.system("git push")


if __name__ == "__main__":
    main()
