import subprocess as sub
import sys, traceback, time
from os.path import normpath, basename
from os import chdir

try:
	# clone the repo and cd into it, if there's given a repo
	if len(sys.argv) > 1:
		repo = sub.check_output(["git", "clone", sys.argv[1]])
		repo_name = basename(normpath(sys.argv[1]))
		chdir(repo_name)

	stamp = time.time()

	# open file to write info into it
	f = open("repo_info_a24.txt", "w")

	# get output from shell
	files = sub.check_output("git ls-files", shell=True)

	# split paths and remove last path which is invalid
	files_paths = files.splitlines()
	files_paths = files_paths[:-1]

	print('Work is in progress ...')

	# get number of commits for each path
	for path in files_paths:
		stats = sub.check_output("git log --all --numstat --oneline --format='%ae' '" + path.decode('utf-8') + "'", shell=True)
		commits = stats.splitlines()

		# empty dictionary and list
		authors = []
		dic = {}

		author = ''
		for i in range(len(commits)):
			commit = commits[i].decode('utf-8').split()
			additions = 0
			
			if len(commit) == 1:
				author = commit[0]
			elif len(commit) == 3:
				if commit[0] != '-':
					additions = int(commit[0])

					if author in dic:
						dic[author] = dic.get(author) + additions
					else:
						dic[author] = additions

		if dic != {}:
			# sort the dictionary and get the author with the most additions
			sorted_dict = sorted(dic.items(), key=lambda x: x[1], reverse=True)
			f.write('Entity {0} - (Author, Number of additions): {1}\n'.format(path.decode('utf-8'), sorted_dict[0]))

	f.close()
	print('Entire process took ' + str(int(time.time() - stamp)) + ' seconds.')
except:
	traceback.print_exc(file=sys.stdout)