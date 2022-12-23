# 사용자 환경변수 설정
> java / hadoop / spark / python

```bash
sudo vim ~/.bashrc

# java
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# java (라즈베리파이)
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

# hadoop
export HADOOP_HOME=/usr/local/hadoop
export HADOOP_COMMON_HOME=$HADOOP_HOME
export HADOOP_HDFS_HOME=$HADOOP_HOME
export HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
export YARN_CONF_DIR=$HADOOP_HOME/etc/hadoop
export HADOOP_YARN_HOME=$HADOOP_HOME
export HADOOP_MAPRED_HOME=$HADOOP_HOME

# spark
export SPARK_HOME=/usr/local/spark

# python & pySpark
export PYTHONPATH=/usr/bin/python3
export PYSPARK_PYTHON=/usr/bin/python3

source ~/.bashrc