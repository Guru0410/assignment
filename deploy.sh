docker build -t cribl .
docker run -v IMAGE --name target cribl node app.js target &
until [ "`docker inspect -f {{.State.Running}} target`"=="true" ]; do
    sleep 0.1;
done;
docker run -v IMAGE --add-host target_1:172.17.0.2 --add-host target_2:172.17.0.2 cribl node app.js splitter &
