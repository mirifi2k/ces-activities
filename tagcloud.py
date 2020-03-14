from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import subprocess as sub
import re, time, sys

if len(sys.argv) > 1:
	repo = sub.check_output(["git", "clone", sys.argv[1]])
	repo_name = basename(normpath(sys.argv[1]))
	chdir(repo_name)

print('Work is in progress ...')
stamp = time.time()

# get commits
ps = sub.Popen(("git", "log", "--all", "--format=%B"), stdout=sub.PIPE)
ret = sub.check_output(["tr", "-d", "'\n'"], stdin=ps.stdout)

# be sure that the result is a string
ret = str(ret)

# split into tokens using a word regex
tokens = re.findall(r'\w+', ret)
string = ' '

# set up tagcloud string
for word in tokens:
	string = string + word.lower() + ' '

# generate tag cloud and show as a figure
tagcloud = WordCloud(width = 800, height = 600,
	background_color='white',
	stopwords = set(STOPWORDS),
	min_font_size=10).generate(string)

print('Took ' + str(int(time.time() - stamp)) + ' seconds to generate the tag cloud (' + str(len(tokens)) + ' words).')

plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(tagcloud)
plt.axis("off")
plt.tight_layout(pad = 0)

plt.show()