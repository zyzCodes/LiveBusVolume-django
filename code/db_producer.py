import json
import dotenv
import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.common.watermark_strategy import WatermarkStrategy

from google.cloud import firestore 

def write_to_firestore(message):

    # Lazily initialize the Firestore client and collection
    if not hasattr(write_to_firestore, "collection_ref"):
        client = firestore.Client(project="livebusvolume")
        write_to_firestore.collection_ref = client.collection("data")
    try:
        data = json.loads(message)
        write_to_firestore.collection_ref.add(data)
        print(f"Inserted into Firestore: {data.keys()}")
    except Exception as e:
        print("Error writing to Firestore:", e)
    return message


def execute(env_file_path):
    # Load environment variables from the .env file.
    environ_vars = dotenv.dotenv_values(env_file_path)

    try:
        broker = environ_vars["bootstrap"]
        api_key = environ_vars["api_key"]
        api_secret = environ_vars["api_secret"]
        input_topic = environ_vars["input_topic"]
        output_topic = environ_vars["output_topic"]
    except Exception as e:
        raise Exception("Env. variables not properly accessed.") from e

    # Set up the Flink execution environment.
    env = StreamExecutionEnvironment.get_execution_environment()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    jar_file = os.path.join(current_dir, "flink-sql-connector-kafka-1.17.2.jar")
    env.add_jars("file://" + jar_file)
    env.set_parallelism(1)

    # Build the Kafka source.
    source = KafkaSource.builder()\
        .set_bootstrap_servers(broker)\
        .set_topics(input_topic)\
        .set_group_id("tensorflow_consumer")\
        .set_value_only_deserializer(SimpleStringSchema())\
        .set_starting_offsets(KafkaOffsetsInitializer.earliest())\
        .set_properties({
            "security.protocol": "SASL_SSL",
            "sasl.mechanism": "PLAIN",
            "sasl.username": api_key,
            "sasl.password": api_secret,
            "sasl.jaas.config": (
                'org.apache.flink.kafka.shaded.org.apache.kafka.common.security.plain.PlainLoginModule required '
                f'username="{api_key}" '
                f'password="{api_secret}";'
            ),
            "ssl.endpoint.identification.algorithm": "https",
            "connections.max.idle.ms": "30000",
            "reconnect.backoff.ms": "1000",
            "reconnect.backoff.max.ms": "10000"
        })\
        .build()

    watermark_strategy = WatermarkStrategy.for_monotonous_timestamps()
    ds = env.from_source(source, watermark_strategy=watermark_strategy, source_name="kafka_source")

    # Process each message to write to Firestore.
    processed_ds = ds.map(write_to_firestore)

    # Execute the streaming job.
    env.execute(job_name="demo")

if __name__ == "__main__":
    execute(".env")
