cd SRE-portfolio

git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate

pip install --upgrade pip

pip install -r requirements.txt

systemctl daemon-reload

systemctl restart myportfolio
