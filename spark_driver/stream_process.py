from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext, RDD
from pyspark.streaming import StreamingContext

from triple import Triple
from preprocess import gen_triple
from typing import List
from config import PATH


def stream_process(trans_func_var, output_func_var):
    print("START NE")
    sc = SparkContext("local[2]", "NetworkWordCount")
    ssc = StreamingContext(sc, 1)
    data_stream = ssc.textFileStream(PATH.DATA_dIR)
    print(PATH.DATA_dIR)
    data_stream.flatMap(trans_func_var)\
               .foreachRDD(lambda rdd_data: rdd_data.foreachPartition(lambda partition_data: push_to_neo4j(output_func_var)))
    ssc.start()
    ssc.awaitTermination()


def trans_func(text: str) -> List[Triple]:
    try:
        print('START MAPPING')
        triple_list = gen_triple(text)
        print("MAPPPPPPPPPPPING ", triple_list)
        return [Triple.map_from_list(t) for t in triple_list]
    except Exception:
        print("ERROR MAPPING")
        return []


def push_to_neo4j(partition: Triple):
    print("OUTPUTDIJNG ")
    print(partition)
    # pass 

