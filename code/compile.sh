# Steps when building the pom for a new bigstitcher version:
# 1. manually copy resources
# 2. edit the pom to comment the "provided" line and the SNAPSHOT for n5-aws-s3
# After compiling, run ./install; create the fat jar by editing
# create-fusion-container-fatjar or copying from a previous version.


export JAVA_HOME=/code/zulu8.80.0.17-ca-fx-jdk8.0.422-linux_x64/jre
export PATH=/code/zulu8.80.0.17-ca-fx-jdk8.0.422-linux_x64:$PATH

apt-get update
apt-get install libblosc-dev

export AWS_REGION=us-west-2

#cd code/bigdataviewer-core
#mvn clean install

#cd ../multiview-reconstruction
#mvn -Denforcer.skip=true clean install

#cd multiview-reconstruction
#mvn clean install 

cd n5-aws-s3
mvn clean install 

#cd ../BigStitcher-Spark_April11_Duplicate

cd ../BigStitcher-Spark_March2025
#mvn -Denforcer.skip=true clean install
mvn -Denforcer.skip=true clean package -P fatjar

##cp ~/.m2/repository/net/preibisch/BigStitcher-Spark/0.0.2-SNAPSHOT/BigStitcher-Spark-0.0.2-SNAPSHOT.jar ../../scratch/

# Build the fat jar (requires the blosc libraries in the Java resources).
mvn clean package -U -P fatjar