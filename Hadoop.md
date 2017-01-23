# SET UP
ssh trung@ec2-52-213-241-169.eu-west-1.compute.amazonaws.com -p 22
hdfs dfs -ls /user/
hdfs dfs -mkdir user/trung

wget https://github.com/wardviaene/hadoop-ops-course/archive/master.zip -O master.zip
unzip master.zip

wget http://search.maven.org/remotecontent?filepath=org/apache/hadoop/hadoop-mapreduce-examples/2.7.3/hadoop-mapreduce-examples-2.7.3.jar -O hadoop-mapreduce-examples-2.7.3.jar

hdfs dfs -put hadoop-mapreduce-examples-2.7.3.jar

mv hadoop-ops-course-master/* hadoop/
hadoop fs -put hadoop/data/constitution.txt

> Word Count
less hadoop/data/
wc -l hadoop/data/names.csv
wc -w hadoop/data/names.csv


# YARN
yarn jar hadoop-mapreduce-examples-2.7.3.jar
yarn jar hadoop-mapreduce-examples-2.7.3.jar wordcount constitution.txt wordcount_output
hdfs dfs -ls wordcount_output
wc -w constitution.txt

# BLUE PRINT
cat scripts/create_blueprint.sh

# PUT FILE (to user/trung)
hdfs dfs -put my-map-reduce

# HIVE
beeline
jdbc:hive2://ec2-52-214-216-145.eu-west-1.compute.amazonaws.com:2181,ec2-52-213-241-169.eu-west-1.compute.amazonaws.com:2181,ec2-52-211-98-209.eu-west-1.compute.amazonaws.com:2181/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2

SHOW databases;
USE db_trung;

CREATE TABLE customers (id INT, firstname STRING, lastname STRING)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '\t'
STORED AS TEXTFILE;

INSERT INTO customers (id, firstname, lastname) VALUES (1, 'John', 'Smith');
INSERT INTO customers (id, firstname, lastname) VALUES (2, 'Bob', 'Smith');
INSERT INTO customers (id, firstname, lastname) VALUES (3, 'Emma', 'Smith');

hadoop fs -put hadoop/data/names-tabs.csv /apps/hive/warehouse/db_trung.db/customers/

> PARTITIONING

> BUCKETING

> UDF: User Defined Functions

> Serialization and Deserialization (Avro, XML, JSON)

> Stringer (ORC) Optimized Row Column
> Change Default file format in Ambari

STORE AS ORC


# PIG
copyFromLocal ./hadoop/data/names.csv names.csv
csv = LOAD 'names.csv' using PigStorage(',') as (firstname:chararray, lastname:chararray);
csv_john = FILTER csv BY firstname == 'JOHN';
csv_john_limit = LIMIT csv_john 3;
DUMP csv_john;
ILLUSTRATE csv_john_limit;

csv_group = GROUP cvs BY lastname;
ILLUSTRATE csv_group;

csv_count = FOREACH csv_group GENERATE group as lastname, COUNT(csv) as count;
ILLUSTRATE csv_count;

STORE csv_count INTO 'csv_count_result' USING PigStorage(',');
quit

# SPARK
pyspark
text_file = sc.textFile("hdfs:///user/trung/constitution.txt")
counts = text_file.flatMap(lambda line: line.split(" ")) \
    .map(lambda word: (word, 2)) \
    .reduceByKey(lambda a, b: a + b)
counts.collect()
counts.saveAsTextFile("hdfs:///user/trung/wordcount_spark_out")

> RDD: Resilient Distributed Dataset
> One block is typically one partition in the RDD
> Transformation: from one RDD to other RDD
> filter
> flatMap: one input many output
> join 2 RDD
> distinct
> repartition
> reduceByKey

rdd.filter(lambda age: age > 18)

> LRU Lease recently userd
> ACTION write back the result to hdfs
> collect: return all elements from RDD to client server
> take (numbers of first elements)
> first
> count, countByValue
> saveAsTextFile
> take, top - sample from result
> reduce

a = [ 1, 2, 3, 4, 6 ]
rdd = sc.parallelize(a)
rdd.filter(lambda element: element > 2).collect()
rdd.map(lambda element: element + 10).take(3)

b = [ (1, 'a'), (2, 'b'), (3, 'c') ]
c = [ (1, 'aa'), (2, 'bb'), (3, 'cc')]
rdd1 = sc.parallelize(b)
rdd2 = sc.parallelize(c)
rdd1.join(rdd2).collect();
rdd1.join(rdd).saveAsTextFile("hdfs:///user/trung/hadoop/joint")

rdd2.map(lambda (k, v): (v, k)).collect(); # Swap key-value
rdd2.map(lambda (k, v): (v, k + 10).filter(lambda (field1, field2): field1 > 10).collect()

jdbc:hive2://ec2-52-214-216-145.eu-west-1.compute.amazonaws.com:2181,ec2-52-213-241-169.eu-west-1.compute.amazonaws.com:2181,ec2-52-211-98-209.eu-west-1.compute.amazonaws.com:2181/;serviceDiscoveryMode=zooKeeper;zooKeeperNamespace=hiveserver2

# SCALA
val logfile="/loudacre/weblogs/2013-09-15.log"
val log = sc.textFile(logfile)
val jpg = log.filter(l => l.contains("jpg"))
jpg.collect()
jpg.count()
val word = jpg.map(j => j.split(" "))
val ips = word.map(ip => p(0))

val activationFiles = sc.wholeTextFiles("/loudacre/activations")
val xml = activationFiles flatMap { case(id, text) => getactivations(text)}

val f = sc.textFile("/loudacre/devicestatus.txt")
val f1 = f.map(f => f.split("\\|")).filter(f => f.length == 14)
val f2 = f1.map(f => (f(0), f(1).split(" "), f(2), f(12), f(13)))
f2.saveAsTextFile("/loudacre/Cleaned2")

val logfile = "/loudacre/weblogs/2013-09-15.log,loudacre/weblogs/2013-09-16.log,loudacre/weblogs/2013-09-17.log"
log.take(2)
val log = sc.textFile(logfile)
val pairRDD = log.map(f => (f.split(" ")(2),1))
pairRDD.take(2)
val reduce = pairRDD.reduceByKey((x,y) => x + y)
val reverse = reduce.map(f => f.swap)
> reduce.map(f => (f.\_2, f.\_1))

val count = reverse.countByKey()

val iplist = log.map(f => (f.split(" ")(2),f.split(" ")(0)))
val Iplist = iplist.groupByKey()
