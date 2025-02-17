"""Way to read frames from a saved video, transmit a batch message containing an array of 5 frames
(with 0.5s between frames), and optionally output each frame to a file."""

import cv2
import lzma
import time
import random
import uuid
import argparse
import json
import numpy as np
import datetime

import client

config: dict = client.read_config()

# Specify your video file path here
vid_path = "bus_camera_footage.mp4"  # Replace with your video file path

def capture(produce: bool, debug: bool, batch_count: int = -1) -> None:
    """
    Read frames from a saved video, collect 5 frames (0.5s between each), 
    and transmit them as a single batch message. If debug is enabled, 
    output each processed frame to a file.
    """
    cap = cv2.VideoCapture(vid_path)
    if not cap.isOpened():
        raise IOError("Error: Could not open video file.")

    # Optionally, print video FPS (not used for batch logic)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25  # fallback if FPS cannot be determined
    print(f"Video FPS: {fps}")

    batch_index = 0

    try:
        while True:
            batch_frames = []
            for i in range(15):
                ret, frame = [cap.read() for i in range(int(fps))][-1]
                if not ret:
                    print("End of video reached.")
                    break

                # Process the frame (crop, encode, compress)
                height, width, _ = frame.shape
                # Crop the bottom-left corner (adjust region as needed)
                bottom_left_corner = frame[:512, 75:512+75]

                ret, jpg_buffer = cv2.imencode('.jpg', bottom_left_corner, [cv2.IMWRITE_JPEG_QUALITY, 90])
                if not ret:
                    print("JPEG encoding failed for a frame, skipping it.")
                    continue

                compressed_bytes = lzma.compress(jpg_buffer.tobytes())

                # If debug is enabled, decode and save both the processed image and original frame
                if debug:
                    decompressed_bytes = lzma.decompress(compressed_bytes)
                    nparr = np.frombuffer(decompressed_bytes, dtype=np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    debug_filename = f"output_batch{batch_index}_frame{i}.jpg"
                    cv2.imwrite(debug_filename, img)
                    orig_filename = f"frame_batch{batch_index}_frame{i}.jpg"
                    cv2.imwrite(orig_filename, frame)
                    print(f"[DEBUG] Saved {debug_filename} and {orig_filename}")

                # Append the compressed frame as a string (for JSON transmission)
                batch_frames.append(str(compressed_bytes))

                # Wait 0.5 seconds before capturing the next frame for the batch
                time.sleep(1)

            # If no frames were captured (e.g., end of video), break out of loop
            if not batch_frames:
                break

            # Send the batch message if producing is enabled
            if produce:
                timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='microseconds')
                message = {
                    'timestamp': timestamp,
                    'frames': batch_frames,
                    'bus_id': str(random.randint(1, 900)),
                    'route_id': random.randint(1, 114)
                }
                if debug:
                    message_size_mb = len(json.dumps(message).encode("utf-8")) / (1024 * 1024)
                    avg_frame_size_mb = message_size_mb / len(batch_frames)
                    print(f"Trying to send batch {batch_index} with {len(batch_frames)} frames at {timestamp}, size: {message_size_mb:.2f} MB, average frame size: {avg_frame_size_mb:.2f} MB")
                client.produce("camera-raw", config, json.dumps(message).encode("utf-8"))
                

            batch_index += 1

            # If a batch_count limit is set, break when reached
            if batch_count >= 0 and batch_index >= batch_count:
                print(f"Reached batch count limit: {batch_count}")
                break

    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Resources released and producer flushed.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Read video frames and send batch messages to Kafka.")
    parser.add_argument('--produce', action='store_true', help="Produce batch messages to Kafka.")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode.")
    parser.add_argument('--batch_count', type=int, default=-1, help="Number of batch messages to transmit.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("Starting producer...", args)
    capture(args.produce, args.debug, args.batch_count)


if __name__ == "__main__":
    main()
