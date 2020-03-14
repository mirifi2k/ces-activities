import subprocess as sub
import sys, time
from os.path import normpath, basename
from os import chdir
from shutil import rmtree

try:
	# clone the repo and cd into it
	if len(sys.argv) > 1:
		repo = sub.check_output(["git", "clone", sys.argv[1]])
		repo_name = basename(normpath(sys.argv[1]))
		chdir(repo_name)

	stamp = time.time()

	# open file to write info into it
	f = open("repo_info_a22.txt", "w")

	# get output from shell
	files = sub.check_output("git ls-files", shell=True)

	# split paths and remove last path which is invalid
	files_paths = files.splitlines()

	if len(files_paths) > 0:
		files_paths = files_paths[:-1]

	print('Work is in progress ...')

	# get number of commits for each path
	for path in files_paths:
		commits = sub.check_output(["git", "log", "--all", "--pretty='%H'", "--follow", "--", path])
		commits = str(commits)

		ps = sub.Popen(("cat", path), stdout=sub.PIPE)
		loc = sub.check_output(["wc", "-l"], stdin=ps.stdout)

		loc = int(loc)
		f.write('Entity {0} has {1} lines of code and {2} commits.\n'.format(path.decode('utf-8'), loc, len(commits.split("\\n"))))

	f.close()
	print('Entire process took ' + str(int(time.time() - stamp)) + ' seconds.')
except:
	print('Unexpected error.')
