import tarfile
from pathlib import Path

_default_files = ("aims.out", "control.in", "geometry.in")

archive = Path("calculations")
outfile = Path(f"{archive}.tgz")

# untar backup.tgz
with tarfile.open("backup.tgz") as tar:
    
    import os
    
    def is_within_directory(directory, target):
        
        abs_directory = os.path.abspath(directory)
        abs_target = os.path.abspath(target)
    
        prefix = os.path.commonprefix([abs_directory, abs_target])
        
        return prefix == abs_directory
    
    def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
    
        for member in tar.getmembers():
            member_path = os.path.join(path, member.name)
            if not is_within_directory(path, member_path):
                raise Exception("Attempted Path Traversal in Tar File")
    
        tar.extractall(path, members, numeric_owner=numeric_owner) 
        
    
    safe_extract(tar)

# save wanted files to calculations.tgz
with tarfile.open(outfile, "w:gz") as tar:
    for file in archive.glob("*"):
        if file.name in _default_files:
            tar.add(file)
