# assignment
The project can be deployed using following script:
**./startDeployment.sh**

The above script will build a docker image and deploy containers for target and splitter. Agent can be triggered using following command:
**docker run -v IMAGE --add-host splitter:172.17.0.3 cribl node app.js agent**

Once the agent has been triggered throughput.csv file can be found and downloaded from the target container.
This file is tracking the input file total bytes, latency (ms) and througput.
**docker exec -it target bash**

The entire setup can be destroyed using following script:
**./destroy.sh**
