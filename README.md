# Quoridor
A repository for my Quoridor game for GLO1901 project\
URL: https://github.com/SamuelYergeau/GLO1901_Projet2

## To setup your Github account:
the commits are evaluated, so make sure we can know who did the commit:
* Use your school email (@ulaval.ca)
* Use your real name as username

## To setup your credentials in VScode:
1. git config --global user.name "[Your name]"
2. git config --global user.email "[your Ulaval email]"
* should eventually prompt you in yout navigator to ask you to connect. Should happen only once.

## To set up the git project:
(à partir d'un nouveau dossier):
1. git init
2. git remote add quoridor https://github.com/SamuelYergeau/GLO1901_Projet2
3. git pull quoridor master
4. git push --set-upstream quoridor master
5. git push quoridor\
Everything should be good and working with that

## To work with GIThub:
1. git pull quoridor
2. git commit -m "[MESSAGE EXPLIQUANT LES MODIFICATIONS APPORTÉES]"
3. git push quoridor

## To open the flow_diagram:
1. go to: https://www.draw.io 
2. click on "open existing project"
3. select "flow_diagram.vsdx"
* If you modify the flow diagram, please export as .vsdx (visio file) and then commit/push to the directory

## VScode extensions to install:
* autoDocstring
* Bracket pair colosizer
* GitLense
* Indent-rainbow
* Live Share
* Live Share Audio
* Live Share Chat
* Live Share Extension Pack
* Python (celle de Microsoft)

## Packages to install:
* pip install requests
* pip install networkx
* pip install -U matplotlib==3.2.0rc1
