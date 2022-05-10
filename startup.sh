python3 Word_Validation_Service/wordsDB.py
python3 Stats_Service/database/stats_db.py
python3 Stats_Service/database/fake_stat_data.py
python3 Stats_Service/update/update.py 
redis-server --daemonize yes

HOME_PATH=$(pwd)
sudo /bin/bash -c 'echo "*/10 * * * * python3 $HOME_PATH/Stats_Service/update/update.py" >> /etc/crontab'

foreman start -e .env -m validate=1,stats=1,answer=1,game_state=1,backend_for_frontend=1 &

./traefik --configFile=traefik.toml
