# DoodleJump
WELCOME
Welcome to my version of Doodle Jump! This is based off of the widely popular 
mobile game, Doodle Jump, where players can control their doodle using arrow keys 
or ‘a’ and ‘d’ keys. There are a variety of platforms to jump on, as well as 
portals that teleport you to a random location. But, beware of the monsters! 
They will hurl globs of radioactive spit at you that will kill you instantly, 
so dodge the bullets and fight back! Best of luck to you and your doodle :D 

RUNNING
To run this project, you can simply navigate to the file “Doodle Jump.py” and 
run it. There were no external modules used that required a demonstration; the 
modules imported can be found at the top of the code in the file “Doodle Jump.py”.

FONTS: 
Be sure that you have the font “Ink Free Regular” installed on your computer. 
(note that because of a bug, I have used the name Ink Free in my code to use 
this font). The .ttf file is included in the same folder that this README 
file was found

SHORTCUTS:
Increase the number of monsters that will spawn:
First comment out “app.monsterProbability = 10 - app.difficulty”
Then, decreasing the number associated with app.monsterProbability will 
increase the likelihood that monsters will spawn. To spawn a monster on every 
platform, change it to 0

Manually Toggle Difficulty:
Comment out “app.difficulty = in (app.score) // 1000”. Then, pressing keys 
1-9 while playing will toggle the difficulty to their corresponding level.

Other than that, the instructions on the tutorial screen should help you gain 
a better understanding of the game mechanics!
