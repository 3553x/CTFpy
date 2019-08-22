Ensure to pick a new secret key when switching to production and to turn off the debugging options!

# Deployment
Log into the admin interface and edit the specified objects.
Some objects only exist for monitoring.

# Category
Add the Categories of the challenges.

# Challenges
Add the Challenges.
Most fields are self-explanatory.
ETA is the estimated time users should take to complete the challenge in minutes.
Rank specifies the order in which the challenges should be unlocked.
Rank must start with 1 and there can't be multiple challenges with the same rank in a category.
Cat specifies the category.
UnlockedBy should be left empty.
Text uses HTML pre tags and isn't escaped.

# ChallengeFile
Allows you to create links for files.
Files are only accessible by logged in users who have unlocked the associated challenge.
fileName is the name shown when downloaded.
localPath is the path on the current system.
remotePath is the path that is appended to the challenge.
e.g.
remotePath = test.txt
challenge = 1
then the file can be downloaded from
localhost/challenges/1/test.txt

# Hint
text is the text to be revealed when the challenge is unlocked.
penalty is the time in minutes that is added to the counter when the challenge is unlocked.

# Team
Users may register on their own but need to be assigned to teams by the admin.
Teams are also created by the admin and should consist of 4 members.

# InfoPost
FAQ like page
add entries if you wish, text isn't escaped and preformatted.

When all teams have been created and the players are ready:
access localhost/challenges/start to start the game by unlocking all rank 1 challenges.

# Mechanisms
Users need to register.
Registration only requires a name and a password.
Users can not participate without a team.

Visitors without account may access stats, info and of course the login and registration pages.

The game can only be started by an administrator, other users tring to access localhost/challenges/start will be laughed at.

Score is calculated the following way:
Each wrong answer is a fixed penalty in minutes.
Each hint is a variable penalty in minutes.
A clock starts ticking the first time a user from a team opens a challenge.
Each team has their own clock.
When the team completes the challenge, the squared estimated time is divided by their needed time plus their penalties to calculate their score.
Score is team based.

