# README.md

# Hadoop and Spark Cluster Configuration with Docker

This project provides a setup for configuring a Hadoop cluster with Spark using Docker. It includes Dockerfiles for building the necessary images, configuration files for Hadoop and Spark, and scripts to start the services.

## Project Structure

```
hadoop-spark-docker
├── docker
│   ├── hadoop
│   │   └── Dockerfile
│   └── spark
│       └── Dockerfile
├── config
│   ├── hadoop
│   │   ├── core-site.xml
│   │   └── hdfs-site.xml
│   └── spark
│       └── spark-defaults.conf
├── scripts
│   ├── start-hadoop.sh
│   └── start-spark.sh
├── docker-compose.yml
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd hadoop-spark-docker
   ```

2. **Build the Docker images:**
   ```bash
   docker-compose build
   ```

3. **Start the services:**
   ```bash
   docker-compose up
   ```

## Usage

- Access the Hadoop services through the specified ports.
- Use the provided scripts to start and manage the Hadoop and Spark services.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.