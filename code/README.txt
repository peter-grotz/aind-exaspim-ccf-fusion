Java + Maven installs handled by linux apt-get.
Checked out BigStitcher-Spark OpenDAL branch.

---- Local Execution ----
(for stitching/grid search)

On 16 CPU, 128 GB machine, compiling bash scripts with 12 CPU and 96 GB:
./install -t 12 -m 96

Scripts are executed in the following order, detect -> match -> solve, progressively adding to an input xml file:
The following flags correspond to Gabor's manifest configs. 
'spark_ip_detections' -> detect-interestpoints
'spark_geometric_descriptor_matching_aff' -> match-interestpoints
'solver_aff' -> solver

./detect-interestpoints -x /data/dataset.xml -l beads -s 4.0 -t 0.0015 --overlappingOnly --storeIntensities --prefetch --minIntensity 0 --maxIntensity 255 -dsxy 4 -dsz 4  --type MAX --localization QUADRATIC --blocksize "1024,1024,1024"
./match-interestpoints -x /data/dataset.xml -l beads -tm AFFINE -rm RIGID --lambda 0.1 -vr OVERLAPPING_ONLY --clearCorrespondences -m PRECISE_TRANSLATION -s 3.0 -r 1 -n 3 -rit 200 -rmir 0.1 -rmif 3.0
./solver -x /data/dataset.xml -s IP -l beads --maxError 5.0 --maxIterations 10000 --maxPlateauwidth 200 --method TWO_ROUND_SIMPLE --relativeThreshold 3.5 --absoluteThreshold 7.0 -fv '0,7' -rtp TIMEPOINTS_INDIVIDUALLY --splitTimepoints -tm AFFINE -rm RIGID --lambda 0.1

NOTE: 
Bash scripts do not have a flag for the s3 dataset location.
This information is encoded inside the xml file.  


---- Cloud Execution ----
(for optimized fusion)

Apparently, this is all you need to run. 
Hypothetically, the input parameters into EMR are the same as the existing first-wins. 

mvn clean package -P fatjar
