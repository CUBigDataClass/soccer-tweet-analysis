# A mini script to start a kafka queue.

cd $KAFKA_HOME

#start zookeeper
nohup bin/zookeeper-server-start.sh -daemon config/zookeeper.properties &

#start a kafka broker
nohup bin/kafka-server-start.sh config/server.properties &