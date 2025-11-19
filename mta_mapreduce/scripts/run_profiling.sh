#!/bin/bash
################################################################################
# MTA Dataset - Run Data Profiling MapReduce Job
# Executes profiling analysis on MTA ridership data
# Author: Debdeep Naha (dn2491)
# Course: CSGA 2436 - Realtime and Big Data Analytics
################################################################################

set -e  # Exit on error

echo "====================================================================="
echo "Running MTA Dataset Profiling MapReduce Job"
echo "====================================================================="

# Configuration
HDFS_INPUT="/user/$(whoami)/mta_ridership/input"
HDFS_OUTPUT="/user/$(whoami)/mta_ridership/output/profiling"
MAPPER="../profiling/profiling_mapper.py"
REDUCER="../profiling/profiling_reducer.py"

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
    -mapper profiling_mapper.py \
    -reducer profiling_reducer.py \
    -input ${HDFS_INPUT}/MTAAnalysis.csv \
    -output ${HDFS_OUTPUT}

echo ""
echo "====================================================================="
echo "Profiling Job Complete!"
echo "====================================================================="
echo ""
echo "Output location: ${HDFS_OUTPUT}"
echo ""
echo "Fetching results..."
hdfs dfs -ls ${HDFS_OUTPUT}

echo ""
echo "Downloading profiling results to local machine..."
rm -rf ../output/profiling
mkdir -p ../output/profiling
hdfs dfs -get ${HDFS_OUTPUT}/* ../output/profiling/

echo ""
echo "Results saved to: mta_mapreduce/output/profiling/"
echo "====================================================================="
