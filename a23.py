import subprocess as sub
import sys, time
from os.path import normpath, basename
from os import chdir

try:
	# clone the repo and cd into it
	if len(sys.argv) > 1:
		repo = sub.check_output(["git", "clone", sys.argv[1]])
		repo_name = basename(normpath(sys.argv[1]))
		chdir(repo_name)

	stamp = time.time()

	# open file to write info into it
	f = open("repo_info_a23.txt", "w")

	# get output from shell
	files = sub.check_output("git ls-files", shell=True)

	# split paths and remove last path which is invalid
	files_paths = files.splitlines()
	files_paths = files_paths[:-1]

	print('Work is in progress ...')

	# get number of commits for each path
	for path in files_paths:
		commits = sub.check_output("git log --all --pretty='%H %ae' --follow -- '" + path.decode('utf-8') + "'", shell=True).splitlines()
		authors = []

		for c in commits:
			commit, author = c.split()
			authors.append(author)

		# remove duplicates of authors for the same file
		authors = list(dict.fromkeys(authors))

		# write into the file
		f.write('Entity {0} has {1} authors and {2} commits.\n'.format(path.decode('utf-8'), len(authors), len(commits)))

	f.close()
	print('Entire process took ' + str(int(time.time() - stamp)) + ' seconds.')
except:
	print('Unexpected error.')