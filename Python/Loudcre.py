from pyspark import SparkConf, SparkContext

conf = SparkConf().setMaster("local").setAppName("Loudacre")
sc = SparkContext(conf = conf)

def parseLine(line):
    fields = line.split('\\|')
    return (fields)

def getvalue(field):
    date = field[0]
    # split manufacturer and model name
    model = field[1].split(" ")
    deviceID = field[2]
    lat = field[3]
    lon = field[4]
    return (date, model, deviceID, lat, lon)

lines = sc.textFile("hdfs:/loudacre/devicestatus.txt")
rdd1 = lines.map(parseLine).filter(lambda x: len(x) == 14)
rdd2 = rdd1.map(getvalue)
results = rdd2.collect()

for result in results:
    print(result)
