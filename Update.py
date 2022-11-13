# This file is used to update the git repository
import json
import os
import datetime


def main():
    # read the package.json file
    with open("package.json", "r") as f:
        currentData = json.load(f)

        isMinorUpdate = input("Is this a minor update? (y/n): ")
        if isMinorUpdate == "y":
            currentData["version"]["minor"] += 1
            currentData["version"]["patch"] = 0
        else:
            currentData["version"]["patch"] += 1

        changeMessage = ""

        addedChanges = []
        addedChange = input("Added changes (d/Done to finish): ")
        while (addedChange != "d" and addedChange != "D"
               and addedChange != "done" and addedChange != "Done"):
            addedChanges.append(addedChange)
            addedChange = input("Added changes (d/Done to finish): ")

        changedChanges = []
        changedChange = input("Changed changes (d/Done to finish): ")
        while (changedChange != "d" and changedChange != "D"
                and changedChange != "done" and changedChange != "Done"):
            changedChanges.append(changedChange)
            changedChange = input("Changed changes (d/Done to finish): ")

        fixedChanges = []
        fixedChange = input("Fixed changes (d/Done to finish): ")
        while (fixedChange != "d" and fixedChange != "D"
                and fixedChange != "done" and fixedChange != "Done"):
            fixedChanges.append(fixedChange)
            fixedChange = input("Fixed changes (d/Done to finish): ")

        removedChanges = []
        removedChange = input("Removed changes (d/Done to finish): ")
        while (removedChange != "d" and removedChange != "D"
                and removedChange != "done" and removedChange != "Done"):
            removedChanges.append(removedChange)
            removedChange = input("Removed changes (d/Done to finish): ")

        # current date
        now = datetime.datetime.now()
        currentData["lastChange"] = now.strftime("%Y-%m-%d")

        versionAsString = f"{currentData['version']['major']}."
        versionAsString += f"{currentData['version']['minor']}."
        versionAsString += f"{currentData['version']['patch']}"
        # write the changes to the changelog
        with open("CHANGELOG.md", "a") as f:
            # append change to end
            f.write(f"## [{versionAsString}] - {currentData['lastChange']}")

            if (len(addedChanges) > 0):
                f.write("### Added")
                for change in addedChanges:
                    f.write(f"  - {change}")

            if (len(changedChanges) > 0):
                f.write("### Changed")
                for change in changedChanges:
                    f.write(f"  - {change}")

            if (len(fixedChanges) > 0):
                f.write("### Fixed")
                for change in fixedChanges:
                    f.write(f"  - {change}")

            if (len(removedChanges) > 0):
                f.write("### Removed")
                for change in removedChanges:
                    f.write(f"  - {change}")

        # write the new version to the package.json file
        with open("package.json", "w") as f:
            json.dump(currentData, f, indent=2)

        changeMessage = f"v{versionAsString} - {currentData['lastChange']}"
        os.system("git add .")
        os.system(f"git commit -m \"{changeMessage}\"")
        os.system("git push")


if __name__ == "__main__":
    main()
