from git import Repo
import random
from slacker import Slacker
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--token")
parser.add_argument("--repo", action='append')

args = parser.parse_args()

commits = []
for repo in args.repo:
    repo = Repo(repo)
    assert not repo.bare

    commits += list(repo.iter_commits())

commits = [c for c in commits
           if "Merge branch" not in c.message
           and "Adding new branch" not in c.message
           and "[maven-release-plugin]" not in c.message
           and "Preparing merge on master" not in c.message
           and "Bump to version" not in c.message
           ]
slack = Slacker(args.token)
chan = "#gitquiz"


while True:
    commit = random.choice(commits)
    slack.chat.post_message(chan, "Qui a commité \n> %s" % commit.message)
    time.sleep(50)
    slack.chat.post_message(chan, "10 secondes restantes...")
    time.sleep(7)
    for i in (3, 2, 1):
        s = "s" if i > 1 else ""
        slack.chat.post_message(chan, "%i seconde%s restante%s..." % (i, s, s))
        time.sleep(1)

    slack.chat.post_message(chan, "Le coupable était: %s" % commit.author.email)
    time.sleep(30)
