git add .
SET /P commitmsg = "Enter a commit message inside of "" "
git commit -m %commitmsg%
