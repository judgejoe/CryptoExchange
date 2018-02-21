xargs -a <(awk '! /^ *(#|$)/' "debs.txt") -r -- sudo apt-get install
pip install -r requirements.txt
sqlite3 cryptoexchange.db < ../db/create_db.sqlite 
sqlite3 cryptoexchange.db < ../db/insert_data.sqlite 
