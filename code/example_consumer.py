import client
import pickle
import lzma
import numpy as np
import cv2

from confluent_kafka import Consumer


def consume():
    config = client.read_config()
    topic = "camera-raw"
    msg = client.consume(topic, config)
    message = pickle.loads(msg.value())

    decompressed_bytes = lzma.decompress(message['frame'])

    # Convert the bytes back to a NumPy array and decode the JPEG image
    jpg_array = np.frombuffer(decompressed_bytes, dtype=np.uint8)
    image = cv2.imdecode(jpg_array, cv2.IMREAD_COLOR)

    # Now you can work with 'image'
    cv2.imwrite("consumed_image.jpg", image)

def main():
    consume()

main()