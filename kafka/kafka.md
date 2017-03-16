## Kakfa on AWS

The bin directory hosts a number of scripts to communicate with kafka. Here is a handful of helpful commands 
for reference. First install kafka by

`wget http://apache.mesi.com.ar/kafka/0.10.2.0/kafka_2.11-0.10.2.0.tgz`

`tar -xzf kafka_2.11-0.10.2.0.tgz`
`sudo cp kafka_2.11-0.10.2.0 /opt/kafka_2.11-0.10.2.0`
`export KAFKA_HOME=/opt/kafka_2.11-0.10.2.0`
`export PATH=$PATH:$KAFKA_HOME/bin`


`cd $KAFKA_HOME`

local$ `scp Party-Parrots/kafka/kafka_start.sh -i id_rsa <user>@52.14.146.157:~`

<user>@52.14.146.157$ `cp kafka_start.sh $KAFKA_HOME`

There is a script $KAFKA_HOME/kafka_start.sh which should run the following commands:

#### To start zookeeper
`sudo nohup bin/zookeeper-server-start.sh -daemon config/zookeeper.properties &`

Note that the zookeeper.properties file is where zookeeper IP:port is configured.

#### To check if zookeeper is running
`echo ruok | nc 127.0.0.1 2181` should return *imok* 
 
#### To start a kafka broker
`bin/kafka-server-start.sh config/server.properties`

Note that the server.properties file is where broker IP:ports are configured.


###### Additional commands

#### To create a topic
`bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic <test>`

#### To list the topics 
`bin/kafka-topics.sh --list --zookeeper localhost:2181`

#### To create a producer on the same server open another ssh session and commit messages there.
`nohup bin/kafka-console-producer.sh --broker-list localhost:9092 --topic <test> &`

#### To read messages from a topic create a consumer on the topic in another ssh session.
`bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic <test> --from-beginning`
