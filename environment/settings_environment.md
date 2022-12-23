# 환경변수 세팅
>  java / hadoop / spark / python

```bash
sudo vim /etc/environment

# PATH 추가
## java
":/usr/lib/jvm/java-11-openjdk-amd64/bin"
## java (raspberry)
"/usr/lib/jvm/java-11-openjdk-arm64/bin"

## hadoop
":/usr/local/hadoop/bin:/usr/local/hadoop/sbin"

## spark
":/usr/local/spark/bin:/usr/local/spark/sbin"

## python
":/usr/bin/python3"

# HOME 경로 설정
## java
JAVA_HOME="/usr/lib/jvm/java-11-openjdk-arm64"

## hadoop
HADOOP_HOME="/usr/local/hadoop"

## spark 
SPARK_HOME="/usr/local/spark"

source /etc/environment
```