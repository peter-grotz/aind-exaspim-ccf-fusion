#Things to change when you download a new version of bigstitcher to make a pom file:
#1. manually copy resources
#2. edit pom file to comment the "provided" line and the SNAAPSHOT for n5-aws-s3
# after compiling, run ./install and you can create the fat jar executable by editing create-fusion-container-fatjar or copy from previous version


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

#copied blosc libraries to java resources (sebastian's notes in email on Nov 2024)
mvn clean package -U -P fatjar