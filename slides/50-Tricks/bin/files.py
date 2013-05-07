from os         import remove, path, getcwd, system, listdir, mkdir
from os.path    import isfile, isdir, join
from sys        import stdin

# Create the absolute path name from a relative path name
def path_name (relative_filename):
    return path.join(getcwd(), relative_filename)

def read_input():
    return [line[:-1] for line in stdin.readlines()]

# Read lines from a file and strip off the tailing newline
def read_file(filename):
    f=open(filename)
    results = [line[:-1] for line in f.readlines()]
    f.close()
    return results

# Write lines of text to a file
def write_file(filename, lines):
    f=open(filename, "w")
    f.write("\n".join(lines)+"\n")
    f.close()
 
# Delete a relative path name   
def delete_file(filename):  
    remove(filename)

# Return the files as a list
def list_files(directory):
    return [ f for f in listdir(directory) if isfile(join(directory, f)) ]

# Return the files as a list
def list_dirs(directory):
    return [ f for f in listdir(directory) if isdir(join(directory, f)) ]

# Print the count and directory name
def count_files(directory):
    print len(list_files(directory)), directory
 
# Check to see if this file or directory exists
def exists(filepath):
    return path.exists(filepath)

# Create the directory if needed
def create_directory(directory):
    if  not exists(directory):
        mkdir (directory)

# Print a flat list
def print_list (list):
    for f in list:
        print f

# Print a list two levels deep
def print_list2 (list):
    for v in list:
        for f in v:
            print f,
        print
