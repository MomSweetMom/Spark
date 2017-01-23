# Correction TP-SPARK-CORE-1

## Prepare you VM

1.
```
[training@localhost ~]$ ~/scripts/sparkdev/training_setup_sparkdev.sh
```

## Use the Spark Shell

2.
```
[training@localhost ~]$ spark-shell
```

3.
```
scala> sc
```

4.
```
scala> sc. [TAB]
```

5.
```
scala> exit
```

## Use RDDs to transform a dataset

6.
```
[training@localhost ~]$ cat /home/training/training_materials/sparkdev/data/frostroad.txt
```

7.
```
[training@localhost ~]$ spark-shell
```

8.
```
scala> val myFile = sc.textFile("file:/home/training/training_materials/sparkdev/data/frostroad.txt")
```

9.
Spark has not read the file yet because of lazy evaluation

10.
```
scala> myFile.count()
```

11.
```
scala> myFile.collect()
```

12.
```
scala> myFile. [TAB]
scala> exit
```

13.
```
[training@localhost ~]$ cat /home/training/training_materials/sparkdev/data/weblogs/2014-03-15.log
```

14.
```
[training@localhost ~]$ hdfs dfs -mkdir /loudacre
[training@localhost ~]$ hdfs dfs -put /home/training/training_materials/sparkdev/data/weblogs /loudacre
[training@localhost ~]$ hdfs dfs -ls /loudacre
```

15.
```
[training@localhost ~]$ spark-shell
scala> val logfile="/loudacre/weblogs/2013-09-15.log"
```

16.
```
scala> val myLogFile = sc.textFile(logfile)
```

17.
```
scala> val jpglogs = myLogFile.filter(line => line.contains(".jpg"))
```

18.
```
scala> sc.textFile(logfile).filter(line => line.contains(".jpg")).count()
```

19.
```
scala> myLogFile.map(line => line.length())
```

20.
```
scala> myLogFile.map(line => line.split(" "))
```

21.
```
scala> ips = myLogFile.map(line => line.split(" ")(0))
```

22.
```
scala> ips.collect().foreach(ip => println(ip))
```

23.
```
scala> ips.saveAsTextFile("/loudacre/iplist")
```

24.
```
scala> sc.textFile("/loudacre/weblogs/*").map(line => line.split(' ')(0)).saveAsTextFile("/loudacre/iplist_entire")
```

25.
```
val logs = sc.textFile("/loudacre/weblogs/*")
var htmllogs=logs.filter(_.contains(".html")).map(line => (line.split(' ')(0),line.split(' ')(2)))
htmllogs.take(5).foreach(t => println(t._1 + "/" + t._2))
```
