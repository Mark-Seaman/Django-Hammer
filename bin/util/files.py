from os         import remove, path, getcwd, system, listdir, mkdir, environ, walk, access, W_OK
from os.path    import isfile, isdir, join, dirname, exists, getsize, getmtime
from sys        import stdin
from subprocess import Popen,PIPE
from glob import glob


# Check if this file is writable
def is_writable(path):
    return access(dirname(path), W_OK) and  (not exists(path) or access(path, W_OK)) 

# Recursive list
def recursive_list(d):
    matches = []
    for root, dirnames, filenames in walk(d):
        for filename in filenames:
            matches.append(join(root, filename).replace(d+'/',''))
    return matches

# Get a file list sorted by time (recent last)
def time_sort_file(d):
    files = filter(isfile, glob(d + "/*"))
    files.sort(key=lambda x: getmtime(x))
    files = map(lambda p:p.replace(d+'/',''), files)
    return files

# Create the absolute path name from a relative path name
def path_name (relative_filename):
    return join(getcwd(), relative_filename)

# Read the input as lines of text
def read_input():
    return stdin.read().split('\n')

# Read lines from a file and strip off the tailing newline
def read_file(filename):
    if not exists(filename): return [ ]
    f=open(filename)
    results = f.read().split('\n')[:-1]
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
    return sorted([ f for f in listdir(directory) if isfile(join(directory, f)) ])

# Return the files as a list
def list_dirs(directory):
    return sorted([ f for f in listdir(directory) if isdir(join(directory, f)) ])

# Print the count and directory name
def count_files(directory):
    print len(list_files(directory)), directory
 

# Create the directory if needed
def create_directory(directory):
    if not exists(directory):
        create_directory(dirname(directory))
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

# Run the command as a process and capture stdout & print it
def do_command(cmd, input=None):
    if input:
        p = Popen(cmd.split(), stdin=PIPE, stdout=PIPE)
        p.stdin.write(input)
        p.stdin.close()
    else:
        p = Popen(cmd.split(), stdout=PIPE)
    return  p.stdout.read()[:-1]

# Run a grep command and capture output
def grep(pattern,file):
    p = Popen(["grep", pattern, file ], stdout=PIPE)
    return  p.stdout.read()
