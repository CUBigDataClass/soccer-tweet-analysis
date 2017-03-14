## Installing Cassandra 3.10 on an AWS server

* Download and untar Cassandra 3.10 (make sure that Oracle Java 8 is installed on the server)
wget http://apache.mirrors.pair.com/cassandra/3.10/apache-cassandra-3.10-bin.tar.gz -O cassandra.tar.gz
tar -xzvf cassandra.tar.gz

* Create a "cassandra" user 
sudo adduser cassandra

* Move the cassandra installation into the /opt/cassandra/1 directory, where the last '1' represents that we are installing the first node of cassandra on the server. If we were to install multiple nodes of cassandra on the same physical server, then repeat this process and have installations in folders 2, 3 and so on.
sudo cp -r cassandra/. /opt/cassandra/1

* Change the owner of the installation directory to the "cassandra" user
sudo chown -R cassandra:cassandra /opt/cassandra

* Add cassandra folders in /var/log and /var/run for the log and pid files respectively and change permissions on the folder
sudo mkdir /var/log/cassandra
sudo mkdir /var/run/cassandra

sudo chown -R cassandra:cassandra /var/log/cassandra
sudo chown -R cassandra:cassandra /var/log/cassandra

* Add the init.d script from GitHub to the /etc/init.d folder. Again the 1 in 'cassandra-1' represents that the init script is dedicated to the first cassandra node. If there are more than 1 nodes, you need to have those many init scripts named cassandra-2, cassandra-3 and so on.
sudo cp cassandra-1 /etc/init.d/cassandra-1
sudo chmod a+x /etc/init.d/cassandra-1

* Test if you can spin up and stop the cassandra server with
sudo service cassandra-1 start
sudo service cassandra-2 status
sudo service cassandra-3 stop

* If you want to use the cqlsh, then cd into the installation directory and use the binary to start the shell
cd /opt/cassandra/1/bin
sudo su - cassandra
./cqlsh

* You can also start/stop the cassandra server from here
cd /opt/cassandra/1/bin
sudo su - cassandra
./cassandra
