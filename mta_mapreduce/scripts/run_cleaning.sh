#!/bin/bash
################################################################################
# MTA Dataset - Run Data Cleaning MapReduce Job
# Executes data cleaning and standardization on MTA ridership data
# Author: Debdeep Naha (dn2491)
# Course: CSGA 2436 - Realtime and Big Data Analytics
################################################################################

set -e  # Exit on error

echo "====================================================================="
echo "Running MTA Dataset Cleaning MapReduce Job"
echo "====================================================================="

# Configuration
HDFS_INPUT="/user/$(whoami)/mta_ridership/input"
HDFS_OUTPUT="/user/$(whoami)/mta_ridership/output/cleaned"
MAPPER="../cleaning/cleaning_mapper.py"
REDUCER="../cleaning/cleaning_reducer.py"

# Check if mapper and reducer exist
if [ ! -f "${MAPPER}" ]; then
    echo "Error: Mapper not found at ${MAPPER}"
    exit 1
fi

if [ ! -f "${REDUCER}" ]; then
    echo "Error: Reducer not found at ${REDUCER}"
    exit 1
fi

# Make scripts executable
chmod +x ${MAPPER}
chmod +x ${REDUCER}

echo "Input: ${HDFS_INPUT}"
echo "Output: ${HDFS_OUTPUT}"
echo ""

# Remove output directory if it exists
echo "Cleaning previous output..."
hdfs dfs -rm -r -f ${HDFS_OUTPUT}

echo "Starting MapReduce job..."
echo ""

# Run MapReduce job using Hadoop Streaming
hadoop jar ${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files ${MAPPER},${REDUCER} \
    -mapper cleaning_mapper.py \
    -reducer cleaning_reducer.py \
    -input ${HDFS_INPUT}/MTAAnalysis.csv \
    -output ${HDFS_OUTPUT}

echo ""
echo "====================================================================="
echo "Cleaning Job Complete!"
echo "====================================================================="
echo ""
echo "Output location: ${HDFS_OUTPUT}"
echo ""
echo "Fetching results..."
hdfs dfs -ls ${HDFS_OUTPUT}

echo ""
echo "Downloading cleaned data to local machine..."
rm -rf ../output/cleaned
mkdir -p ../output/cleaned
hdfs dfs -get ${HDFS_OUTPUT}/* ../output/cleaned/

echo ""
echo "Cleaned data saved to: mta_mapreduce/output/cleaned/"
echo ""
echo "Preview of cleaned data (first 10 lines):"
head -10 ../output/cleaned/part-00000

echo ""
echo "====================================================================="
