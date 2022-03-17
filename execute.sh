dt=$(date)

echo "Executed on/at ${date}" >> ~/ages_age/covid-age-bl/execute.log

cd /home/ubuntu/ages_age/covid-age-bl/

git pull
echo "$dt [INFO] git pull done"

python3 ages_age_bl_standalone.py
echo "$dt [INFO] ages age done"

#python3 ages_age_bl_standalone_full.py

#echo "$dt [INFO] ages age FULL done"

dat=$(date)


git commit -am "$dat"
echo "git commit done $dat"

git push

echo "[INFO] pushed"

