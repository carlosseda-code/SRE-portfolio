tmux kill-session -t my_session

cd SRE-portfolio

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

tmux new-session -d -s my_session 'flask run --host=0.0.0.0'
