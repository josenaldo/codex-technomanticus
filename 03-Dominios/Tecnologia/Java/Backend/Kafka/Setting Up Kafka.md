- [[#Start Zookeeper and Kafka Broker]]
- [[#How to create a topic ?]]
- [[#How to Delete a Kafka Topic?]]
- [[#How to instantiate a Console Producer?]]
    - [[#Without Key]]
    - [[#With Key]]
- [[#How to instantiate a Console Consumer?]]
    - [[#Without Key]]
    - [[#With Key]]
    - [[#With Consumer Group]]
- [[#Setting Up Multiple Kafka Brokers]]
    - [[#Starting up the new Broker]]
- [[#Advanced Kafka CLI operations:]]
    - [[#List the topics in a cluster]]
    - [[#Describe topic]]
    - [[#Alter the min insync replica]]
    - [[#Delete a topic]]
    - [[#How to view consumer groups]]
    - [[#Consumer Groups and their Offset]]
    - [[#Viewing the Commit Log]]

  

> [!important] Make sure you are inside the
> 
> **bin/windows** directory.

## Start Zookeeper and Kafka Broker

- Start up the Zookeeper.

```Shell
zookeeper-server-start.bat ..\..\config\zookeeper.properties
```

- Start up the Kafka Broker.

```Shell
kafka-server-start.bat ..\..\config\server.properties
```

## How to create a topic ?

```Shell
kafka-topics.bat --bootstrap-server localhost:9092 --create --topic test-topic --replication-factor 1 --partitions 4 
```

- Topic with Replication Factor as 3.

```Shell
kafka-topics.bat --bootstrap-server localhost:9092 --create --topic test-topic-replicated --replication-factor 3 --partitions 3
```

- Create Items Topic

```Shell
kafka-topics.bat --bootstrap-server localhost:9092 --create --topic items --replication-factor 3 --partitions 3
```

## **How to Delete a Kafka Topic?**

- Delete the topic `test-topic`

```Shell
kafka-topics.bat --bootstrap-server localhost:9092 --delete --topic test-topic
```

## How to instantiate a Console Producer?

### Without Key

```Plain
kafka-console-producer.bat --broker-list localhost:9092 --topic test-topic
```

### With Key

```Plain
kafka-console-producer.bat --broker-list localhost:9092 --topic test-topic --property "key.separator=-" --property "parse.key=true"
```

## How to instantiate a Console Consumer?

### Without Key

```Plain
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test-topic --from-beginning
```

### With Key

```Plain
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test-topic --from-beginning -property "key.separator= - " --property "print.key=true"
```

### With Consumer Group

```Plain
kafka-console-consumer.bat --bootstrap-server localhost:9092 --topic test-topic --group <group-name>
```

## Setting Up Multiple Kafka Brokers

- The first step is to add a new **server.properties**.

- We need to modify three properties to start up a multi broker set up.

```Plain
broker.id=<unique-broker-d>
listeners=PLAINTEXT://localhost:<unique-port>
log.dirs=/tmp/<unique-kafka-folder>
auto.create.topics.enable=false
```

- Example config will be like below.

```Plain
broker.id=1
listeners=PLAINTEXT://localhost:9093
log.dirs=/tmp/kafka-logs-1
auto.create.topics.enable=false
```

### Starting up the new Broker

- Provide the new **server.properties** thats added.

```Plain
./kafka-server-start.sh ../config/server-1.properties
```

```Plain
./kafka-server-start.sh ../config/server-2.properties
```

# Advanced Kafka CLI operations:

> [!important] Make sure you are inside the
> 
> **bin/windows** directory.

## List the topics in a cluster

```Plain
kafka-topics.bat --bootstrap-server localhost:9092 --list
```

## Describe topic

- The below command can be used to describe all the topics.

```Plain
kafka-topics.bat --bootstrap-server localhost:9092 --describe
```

- The below command can be used to describe a specific topic.

```Plain
kafka-topics.bat --bootstrap-server localhost:9092 --describe --topic <topic-name>
```

## Alter the min insync replica

```Plain
kafka-configs.bat --bootstrap-server localhost:9092 --entity-type topics --entity-name test-topic-replicated --alter --add-config min.insync.replicas=2
```

## Delete a topic

```Plain
kafka-topics.bat --bootstrap-server localhost:9092 --delete --topic <topic-name>
```

## How to view consumer groups

```Plain
kafka-consumer-groups.bat --bootstrap-server localhost:9092 --list
```

## Consumer Groups and their Offset

```Plain
kafka-consumer-groups.bat --bootstrap-server localhost:9092 --describe --group console-consumer-27773
```

## Viewing the Commit Log

```Plain
kafka-run-class.bat kafka.tools.DumpLogSegments --deep-iteration --files /tmp/kafka-logs/test-topic-0/00000000000000000000.log
```