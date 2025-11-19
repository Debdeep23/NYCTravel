#!/bin/bash
################################################################################
# MTA Dataset - HDFS Setup Script
# Creates necessary HDFS directory structure
# Author: Debdeep Naha (dn2491)
# Course: CSGA 2436 - Realtime and Big Data Analytics
################################################################################

set -e  # Exit on error

echo "====================================================================="
echo "Setting up HDFS directory structure for MTA Dataset"
echo "====================================================================="

# Define HDFS paths
HDFS_BASE="/user/$(whoami)/mta_ridership"
HDFS_INPUT="${HDFS_BASE}/input"
HDFS_OUTPUT="${HDFS_BASE}/output"
HDFS_PROFILING="${HDFS_OUTPUT}/profiling"
HDFS_CLEANED="${HDFS_OUTPUT}/cleaned"

echo "Creating HDFS directories..."

# Remove existing directories if they exist
hdfs dfs -rm -r -f ${HDFS_BASE}

# Create directory structure
hdfs dfs -mkdir -p ${HDFS_INPUT}
hdfs dfs -mkdir -p ${HDFS_PROFILING}
hdfs dfs -mkdir -p ${HDFS_CLEANED}

echo "HDFS directory structure created successfully!"
echo ""
echo "Directory structure:"
hdfs dfs -ls -R ${HDFS_BASE}

echo ""
echo "====================================================================="
echo "HDFS Setup Complete!"
echo "====================================================================="
