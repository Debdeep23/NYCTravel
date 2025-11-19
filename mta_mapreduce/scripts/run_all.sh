#!/bin/bash
################################################################################
# MTA Dataset - Master Script
# Runs complete data ingestion, profiling, and cleaning pipeline
# Author: Debdeep Naha (dn2491)
# Course: CSGA 2436 - Realtime and Big Data Analytics
################################################################################

set -e  # Exit on error

echo "###################################################################"
echo "#                                                                  #"
echo "#           MTA RIDERSHIP DATA PROCESSING PIPELINE                #"
echo "#                                                                  #"
echo "#  Author: Debdeep Naha (dn2491)                                  #"
echo "#  Course: CSGA 2436 - Realtime and Big Data Analytics            #"
echo "#  Dataset: MTA Subway Hourly Ridership (2020-2024)               #"
echo "#                                                                  #"
echo "###################################################################"
echo ""

START_TIME=$(date +%s)

# Step 1: Setup HDFS
echo "STEP 1: Setting up HDFS directory structure..."
./setup_hdfs.sh
echo ""

# Step 2: Upload data to HDFS
echo "STEP 2: Uploading data to HDFS..."
./upload_to_hdfs.sh
echo ""

# Step 3: Run profiling job
echo "STEP 3: Running data profiling MapReduce job..."
./run_profiling.sh
echo ""

# Step 4: Run cleaning job
echo "STEP 4: Running data cleaning MapReduce job..."
./run_cleaning.sh
echo ""

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

echo "###################################################################"
echo "#                                                                  #"
echo "#                    PIPELINE COMPLETE!                            #"
echo "#                                                                  #"
echo "###################################################################"
echo ""
echo "Total execution time: ${DURATION} seconds"
echo ""
echo "Output locations:"
echo "  - Profiling results: mta_mapreduce/output/profiling/"
echo "  - Cleaned data: mta_mapreduce/output/cleaned/"
echo ""
echo "Next steps:"
echo "  1. Review profiling results"
echo "  2. Analyze cleaned dataset"
echo "  3. Generate report using generate_report.py"
echo ""
echo "###################################################################"
