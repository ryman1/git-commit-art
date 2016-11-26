# git-commit-art
Creates a series of commits that can display pixel art in a github contributions graph. The resulting art is derived from the art.png file. The file can be edited in your chosen photo editor. You must _only_ use the exact 5 shades included in the default art.png file.

**Requirements:** 
- Python 3
- pypng - `pip install pypng`
- git in PATH

Before running the program, be sure to update the "gitemail" setting in **config.json** to match the address of the owner of the github repo (see below).
 
Once **git-commit-art.py** has been run, a folder called 'project' is created which houses the local git repository and the project file which is repeatedly updated to create new commits.

To display the resulting graph on Github:

1. Create a new repo on github (preferably with a throwaway account to avoid interfering with your primary account's stats).

2. cd to the 'project' directory and run `git remote add origin [url to your new github repo]`

3. Run `git push -u origin master`
