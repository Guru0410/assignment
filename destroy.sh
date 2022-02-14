docker container kill $(docker ps -q)
yes | docker system prune -a
