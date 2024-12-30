# start-cluster.sh
#!/bin/bash

# Formater le NameNode (première fois uniquement)
hdfs namenode -format

# Démarrer les services HDFS
start-dfs.sh

# Démarrer les services YARN
start-yarn.sh

# Démarrer Spark
start-master.sh
start-slave.sh spark://sparkmaster:7077

# Garder le processus en premier plan
tail -f /dev/null