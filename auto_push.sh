if [ -z "$1" ]
then
    echo "give me a push message"
    exit 1
else
    cd ~/Desktop/Cours
    git add .
    git commit -m "$1"
    git push
fi

# Ne pas oublier de mettre un alias dans le .bashrc :
# alias push='~/Desktop/Cours/auto_push.sh'