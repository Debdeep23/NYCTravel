# Dataproc Cluster File Transfer Guide

**Author**: Debdeep Naha (dn2491)
**Course**: CSGA 2436 - Realtime and Big Data Analytics

---

## Current Situation

You've already run the MapReduce jobs on your cluster with:
- ✅ `profiling_mapper.py` (working correctly)
- ✅ `profiling_reducer.py` (has aggregation bug)
- ✅ `cleaning_mapper.py` (working correctly)
- ✅ `cleaning_reducer.py` (working correctly)

**Problem**: The profiling reducer doesn't properly aggregate, causing huge outputs.

**Question**: What files do you need on the cluster now?

---

## Decision: Two Options

### ✅ OPTION 1: Keep Existing Outputs + Post-Process Locally (RECOMMENDED)

**Best if**: You want results quickly and don't want to re-run the expensive MapReduce job.

**Files to transfer to cluster**: **NONE** ❌

**What to do**:
1. Keep your existing HDFS outputs as-is
2. Run post-processing scripts **locally** (on your machine, not on cluster)
3. Get your report in 5-10 minutes

**Steps**:
```bash
# On your LOCAL machine (where you have this repo)
cd /home/user/NYCTravel/mta_mapreduce/post_processing
./process_outputs.sh
```

**Pros**:
- ✅ No need to re-run MapReduce job (saves time and money)
- ✅ No file transfers needed
- ✅ Get results immediately
- ✅ Post-processing is fast and local

**Cons**:
- ❌ HDFS still contains the huge profiling output (wastes storage)

---

### ✅ OPTION 2: Fix Reducer + Re-run Profiling Job

**Best if**: You want properly aggregated outputs in HDFS or need to re-run anyway.

**Files to transfer to cluster**: **1 file**

#### File to Upload

**New file**: `mta_mapreduce/profiling/profiling_reducer_fixed.py`

This is the corrected reducer that properly aggregates in memory.

#### Transfer Command

```bash
# From your local machine, upload to your Dataproc cluster
gcloud compute scp \
    /home/user/NYCTravel/mta_mapreduce/profiling/profiling_reducer_fixed.py \
    <your-cluster-master-node>:~/profiling_reducer_fixed.py

# Or if you have direct SSH access:
scp /home/user/NYCTravel/mta_mapreduce/profiling/profiling_reducer_fixed.py \
    username@cluster-ip:~/profiling_reducer_fixed.py
```

#### Re-run Profiling Job

```bash
# SSH into your cluster
gcloud compute ssh <your-cluster-master-node>

# Then run the corrected profiling job
hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -files profiling_mapper.py,profiling_reducer_fixed.py \
    -mapper profiling_mapper.py \
    -reducer profiling_reducer_fixed.py \
    -input /user/dn2491_nyu_edu/MTA_Subway.csv \
    -output /user/dn2491_nyu_edu/mta_profiling_fixed \
    -numReduceTasks 1
```

#### Cleanup Old Output

```bash
# After the new job succeeds, delete the old huge output
hdfs dfs -rm -r /user/dn2491_nyu_edu/mta_profiling_full
```

**Pros**:
- ✅ HDFS contains properly aggregated outputs
- ✅ Smaller output files in HDFS
- ✅ Can skip post-processing step

**Cons**:
- ❌ Need to re-run MapReduce job (time + cost)
- ❌ Need to transfer files

---

## Recommended Choice

### Choose OPTION 1 if:
- ✅ You want results NOW
- ✅ You don't want to re-run the job
- ✅ You're okay with post-processing locally

### Choose OPTION 2 if:
- ✅ You need to re-run the job anyway (for other reasons)
- ✅ You want cleaner HDFS outputs
- ✅ You need the aggregated data accessible from Hive/Trino/other tools on the cluster

---

## What About Cleaning Scripts?

**Your cleaning scripts are fine!** ✅

You don't need to change:
- `cleaning_mapper.py` (working correctly)
- `cleaning_reducer.py` (working correctly)

The cleaning job outputs are already deduplicated and properly formatted.

---

## Summary Table

| Scenario | Files to Transfer | Actions Required |
|----------|------------------|------------------|
| **OPTION 1: Post-process locally** | **None** | Run `./process_outputs.sh` locally |
| **OPTION 2: Fix and re-run** | `profiling_reducer_fixed.py` | Upload file, re-run profiling job |
| **Cleaning jobs** | **None** | Already working correctly ✅ |

---

## File Locations Reference

### Current Files on Cluster

```
~/
├── profiling_mapper.py          (already there ✅)
├── profiling_reducer.py         (already there, but has bug ⚠️)
├── cleaning_mapper.py           (already there ✅)
└── cleaning_reducer.py          (already there ✅)
```

### New File (if choosing Option 2)

```
~/
└── profiling_reducer_fixed.py   (NEW - upload if re-running)
```

### Local Post-Processing Files (for Option 1)

```
/home/user/NYCTravel/mta_mapreduce/post_processing/
├── aggregate_profiling.py       (run locally ✅)
├── generate_report.py           (run locally ✅)
├── process_outputs.sh           (run locally ✅)
└── quick_stats.sh               (run locally ✅)
```

---

## My Recommendation

**Go with OPTION 1** - Post-process locally! 🎯

Why:
1. **Fast**: Get results in 5-10 minutes
2. **Simple**: Just run `./process_outputs.sh`
3. **No cluster changes**: Keep everything as-is
4. **Same end result**: You get the exact same markdown report

You can always fix and re-run later if needed.

---

## Commands for Option 1 (Recommended)

```bash
# Step 1: Navigate to post-processing directory
cd /home/user/NYCTravel/mta_mapreduce/post_processing

# Step 2: Run automated processing
./process_outputs.sh

# Step 3: View your report
cat output_analysis/data_quality_report.md
```

**That's it!** No cluster file transfers needed.

---

## Commands for Option 2 (If You Choose to Re-run)

```bash
# Step 1: Transfer fixed reducer to cluster
gcloud compute scp \
    /home/user/NYCTravel/mta_mapreduce/profiling/profiling_reducer_fixed.py \
    <your-cluster-master>:~/profiling_reducer_fixed.py

# Step 2: SSH into cluster
gcloud compute ssh <your-cluster-master>

# Step 3: Re-run profiling job with fixed reducer
hadoop jar /usr/lib/hadoop/hadoop-streaming.jar \
    -files profiling_mapper.py,profiling_reducer_fixed.py \
    -mapper profiling_mapper.py \
    -reducer profiling_reducer_fixed.py \
    -input /user/dn2491_nyu_edu/MTA_Subway.csv \
    -output /user/dn2491_nyu_edu/mta_profiling_fixed \
    -numReduceTasks 1

# Step 4: Verify output size is smaller
hdfs dfs -du -h /user/dn2491_nyu_edu/mta_profiling_fixed

# Step 5: Download and view results
hdfs dfs -cat /user/dn2491_nyu_edu/mta_profiling_fixed/part-* | head -100

# Step 6: Cleanup old output (optional)
hdfs dfs -rm -r /user/dn2491_nyu_edu/mta_profiling_full
```

---

## Quick Decision Chart

```
Do you need to re-run the profiling job for other reasons?
│
├─ NO  → OPTION 1: Post-process locally ✅ (RECOMMENDED)
│         No cluster changes needed!
│
└─ YES → OPTION 2: Upload profiling_reducer_fixed.py
          Re-run job with fixed reducer
```

---

## Questions?

**Q: Will post-processing locally give me the same report?**
A: Yes! Exactly the same markdown report with all the tables and statistics.

**Q: Should I delete the huge profiling output from HDFS?**
A: Only if storage is a concern. Otherwise, keep it until you've verified the post-processed report looks good.

**Q: What if I want both options?**
A: Do Option 1 first (get results now), then do Option 2 later if needed (cleaner HDFS).

**Q: Is the fixed reducer the same as the aggregate_profiling.py script?**
A: Yes, same logic! One runs on the cluster in Hadoop, the other runs locally on downloaded data.

---

**End of Guide**
