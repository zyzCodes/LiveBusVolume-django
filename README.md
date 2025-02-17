# Smart Transit Real-Time Analytics

A cutting-edge platform that repurposes existing hardware—from agency, city, and government cameras—to deliver real-time public transit analytics. Our solution leverages privacy-preserving object detection to count passengers (without recording personal identities) and processes these counts via a distributed pipeline. Imagine a city like Edmonton tracking bus ridership across 900+ buses in real time to optimize transit operations and resource allocation.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technologies Used](#technologies-used)
- [Benefits](#benefits)
- [Usage](#usage)

---

## Overview

Smart Transit Real-Time Analytics transforms existing camera infrastructure into a powerful tool for modern urban management. By implementing state-of-the-art machine learning models for object detection (focused solely on counting objects to maintain privacy), we provide actionable insights through a fully distributed, real-time pipeline. Our system empowers cities and transit agencies to:

- **Optimize Resources:** Deploy more buses in high-demand areas.
- **Improve Traffic Strategies:** Develop data-driven strategies for smoother traffic flow.
- **Enhance Emergency Response:** Monitor passenger volumes to trigger timely alerts and updates.

---

## Features

- **Real-Time Data Pipeline:** 
  - Ingests live video feeds from cameras installed on buses, trains, or public spaces.
- **Privacy-Preserving Object Detection:** 
  - Only counts individuals without storing or transmitting personal data.
- **Distributed Processing:**
  - Utilizes [Confluent Apache Kafka](https://www.confluent.io/product/kafka-streaming-platform/) for data streaming.
  - Processes streams with [Confluent Apache Flink](https://flink.apache.org/) for real-time analytics.
- **Scalable Dashboard:**
  - Feeds real-time insights to dynamic dashboards, enabling instant visualization.
- **Containerized Deployment:**
  - Uses Docker and GCK (Google Cloud Kubernetes) for seamless scaling and management.

---

## Architecture

1. **Camera Feeds:**  
   Existing hardware captures video streams from transit vehicles or public areas.
   
2. **Data Ingestion via Apache Kafka:**  
   Streams video data into a Kafka cluster, ensuring high-throughput and fault-tolerant delivery.

3. **Real-Time Processing with Apache Flink:**  
   Processes data in real time to run ML object detection models, extracting counts from video frames.

4. **Dashboard Integration:**  
   Processed data is fed into dashboards to display live transit statistics and insights.

> **Diagram (Conceptual):**

```mermaid
flowchart LR
    A[Camera Feeds] --> B[Apache Kafka]
    B --> C[Apache Flink]
    C --> D[ML Object Detection]
    D --> E[Firebase/NoSQL]
    E --> F[Dashboard & Analytics]
