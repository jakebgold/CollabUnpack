import os, pathlib, shutil
import zipfile as zf

# Set these manually before running the program.
# "Rootdir is the directory where all the folders live.
# Assignment is the title of the assignment. It can be whatever you want.
rootdir = "PATH"
assignment = 'HW'

# Deletes stranded .DS_Store files
for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if file.startswith('.DS_STORE') or file.startswith(".DS_Store"):
            os.remove(os.path.join(subdir, file))


# Extracts all ZIP files
manual_checks = []
for subdir, dirs, files in os.walk(rootdir):
    for student in dirs:
        computing_id = student.split("(")[-1].split(")")[0]
        for _, _, zipped_file in os.walk(os.path.join(rootdir, student, 'Submission attachment(s)')):
            if zipped_file[0].endswith('.zip'):
                with zf.ZipFile(os.path.join(rootdir, student, 'Submission attachment(s)', zipped_file[0]), 'r') as zipdata:
                    for zipinfo in zipdata.infolist():
                        preferred_name = computing_id + "_" + assignment + "." + str(zipinfo.filename).split(".")[-1]
                        pref_name_path = pathlib.Path(os.path.join(rootdir, 'all', preferred_name))
                        secondary_name = computing_id + "_" + assignment + "_" + str(zipinfo.filename).split(".")[0] + "." + str(zipinfo.filename).split(".")[-1]

                        if os.path.isfile(os.path.join(rootdir, 'all', preferred_name)) and not os.path.isdir(os.path.join(rootdir, 'all', preferred_name)):
                            zipinfo.filename = secondary_name
                        elif os.path.isdir(os.path.join(rootdir, 'all', preferred_name)):
                            continue
                        else:
                            zipinfo.filename = preferred_name

                        zipdata.extract(zipinfo, path=os.path.join(rootdir, 'all'))
            else:
                os.rename(os.path.join(rootdir, student, 'Submission attachment(s)', zipped_file[0]), os.path.join(rootdir, "all", zipped_file[0]))
    break


# Delete the __MACOSX folders that appear for no real reason
for fname in os.listdir(os.path.join(rootdir, "all")):
    if fname.endswith("__MACOSX"):
        shutil.rmtree(os.path.join(rootdir, 'all', fname))

# Rename files inside the folders and move them into the 'All' folder
dirs = [x[0] for x in os.walk(os.path.join(rootdir, "all"))][1:]

for folder in dirs:
    computing_id = folder.split("all/")[-1].split("_")[0]
    for pth in pathlib.Path(folder).iterdir():
        if pth.is_file():
            preferred_name = computing_id + "_" + assignment + pth.suffix
            pref_name_path = pathlib.Path(os.path.join(rootdir, 'all', preferred_name))
            secondary_name = computing_id + "_" + assignment + "_" + pth.stem + pth.suffix
            secondary_name_path = pathlib.Path(os.path.join(rootdir, 'all', secondary_name))

            if pref_name_path.is_file():
                pth.rename(pathlib.Path(os.path.join(rootdir, "all"), secondary_name))
            else:
                pth.rename(pathlib.Path(os.path.join(rootdir, "all"), preferred_name))
        else:
            print("Error with: " + str(pth))

# Close out the empty folders
for item in dirs:
    shutil.rmtree(item)


# Delete the pesky .DS_STORE files
for subdir, dirs, files in os.walk(os.path.join(rootdir, "all")):
    for file in files:
        if file.endswith('.DS_STORE') or file.endswith(".DS_Store"):
            os.remove(os.path.join(subdir, file))


# Tests to confirm the system is working as expected
for _, _, files in os.walk(os.path.join(rootdir, "all")):
    students_in_all = len(set([x.split("_")[0] for x in files]))


dirs = [x[0] for x in os.walk(rootdir)][1:]

print('1. Students with submissions: ' + str(round((len(dirs) - 1) / 2)))
print("2. Students in 'all' folder: " + str(students_in_all))
print("If line 1 doesn't equal line 2, something went wrong.")

