#!/bin/bash
################################################################################
# MTA Dataset - Upload Data to HDFS
# Uploads the MTA CSV dataset to HDFS
# Author: Debdeep Naha (dn2491)
# Course: CSGA 2436 - Realtime and Big Data Analytics
################################################################################

set -e  # Exit on error

# Configuration
LOCAL_DATA_PATH="../MTAAnalysis.csv"
HDFS_INPUT="/user/$(whoami)/mta_ridership/input"

echo "====================================================================="
echo "Uploading MTA Dataset to HDFS"
echo "====================================================================="

# Check if local file exists
if [ ! -f "${LOCAL_DATA_PATH}" ]; then
    echo "Error: Data file not found at ${LOCAL_DATA_PATH}"
    echo "Please ensure MTAAnalysis.csv is in the correct location"
    exit 1
fi

echo "Local file: ${LOCAL_DATA_PATH}"
echo "HDFS destination: ${HDFS_INPUT}"
echo ""

# Get file size
FILE_SIZE=$(ls -lh ${LOCAL_DATA_PATH} | awk '{print $5}')
echo "File size: ${FILE_SIZE}"

# Upload to HDFS
echo "Uploading data to HDFS..."
hdfs dfs -put ${LOCAL_DATA_PATH} ${HDFS_INPUT}/

echo ""
echo "Upload complete! Verifying..."
hdfs dfs -ls ${HDFS_INPUT}

echo ""
echo "====================================================================="
echo "Data Upload Complete!"
echo "====================================================================="
