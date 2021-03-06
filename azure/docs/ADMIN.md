# Admin notes

## Good Azure docs
https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/virtual-machines/linux/optimization.md
https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/virtual-machines/linux/configure-raid.md
https://github.com/MicrosoftDocs/azure-docs/blob/master/articles/virtual-machines/linux/classic/optimize-mysql.md

## Spark benchmark
Using `N_KEYS = 200; MB_PER_KEY = 500; N_JOBS = 100` in `spark_demo.ipynb`
- Sequential write with `df.write.save("hdfs:///user/ubuntu/bigData.parquet")` (152G)

| Machine          | Disks         | Time         |
| ---------------  |:-------------:|:------------:|
| Standard_DS12_v2 | 4 HDD         | 7.5 min      |
| Standard_DS12_v2 | 4 SSD         | 6.1 min      |
| Standard_DS12_v2 | 4HDD RAID0    | 7.3 min      |
| Standard_E4_v3   | 4HDD RAID0    | 6 min        |

- Flush disks: `parallel-ssh -i -t 0 -H "cluster1 cluster2 cluster3" "sudo sh -c \"sync && echo 3 > /proc/sys/vm/drop_caches\""`
- Sequential read with `ss.read.parquet("hdfs:///user/ubuntu/bigData.parquet").rdd.map(lambda x: len(x)).distinct().count()`

| Machine          | Disks         | Time         |
| ---------------  |:-------------:|:------------:|
| Standard_DS12_v2 | 4 HDD         | 38 min      |
| Standard_DS12_v2 | 4 SSD         | 11 min      |
| Standard_DS12_v2 | 4HDD RAID0    | 12 min      |
| Standard_E4_v3   | 4HDD RAID0    | 13 min      |

- Flush disks again
- Shuffle test with `ss.read.parquet("hdfs:///user/ubuntu/bigData.parquet").groupby("key").agg({"value": "max"}).collect()`

| Machine          | Disks         | Time         |
| ---------------  |:-------------:|:------------:|
| Standard_DS12_v2 | 4HDD RAID0    | 21 min       |
| Standard_E4_v3   | 4HDD RAID0    | 16 min       |


## HDFS benchmark
Write test: `hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-client-jobclient-*-tests.jar TestDFSIO -write -nrFiles 9 -fileSize 10000`

```
18/03/28 22:06:59 INFO fs.TestDFSIO: ----- TestDFSIO ----- : write
18/03/28 22:06:59 INFO fs.TestDFSIO:            Date & time: Wed Mar 28 22:06:59 UTC 2018
18/03/28 22:06:59 INFO fs.TestDFSIO:        Number of files: 9
18/03/28 22:06:59 INFO fs.TestDFSIO: Total MBytes processed: 90000.0
18/03/28 22:06:59 INFO fs.TestDFSIO:      Throughput mb/sec: 113.71892472438955
18/03/28 22:06:59 INFO fs.TestDFSIO: Average IO rate mb/sec: 114.65151977539062
18/03/28 22:06:59 INFO fs.TestDFSIO:  IO rate std deviation: 10.590325290363486
```

Flush disks: `parallel-ssh -i -t 0 -H "cluster1 cluster2 cluster3" "sudo sh -c \"sync && echo 3 > /proc/sys/vm/drop_caches\""`

Read test: `hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-mapreduce-client-jobclient-*-tests.jar TestDFSIO -read -nrFiles 9 -fileSize 10000`

```
18/03/28 22:15:09 INFO fs.TestDFSIO: ----- TestDFSIO ----- : read
18/03/28 22:15:09 INFO fs.TestDFSIO:            Date & time: Wed Mar 28 22:15:09 UTC 2018
18/03/28 22:15:09 INFO fs.TestDFSIO:        Number of files: 9
18/03/28 22:15:09 INFO fs.TestDFSIO: Total MBytes processed: 90000.0
18/03/28 22:15:09 INFO fs.TestDFSIO:      Throughput mb/sec: 63.713115415600655
18/03/28 22:15:09 INFO fs.TestDFSIO: Average IO rate mb/sec: 67.43341064453125
18/03/28 22:15:09 INFO fs.TestDFSIO:  IO rate std deviation: 17.202486986872554
```

## Tools

**(for admin)** Install AzCopy in Windows environment for blobs copy across storage accounts:
https://docs.microsoft.com/en-us/azure/storage/storage-use-azcopy

**(for admin)** Install Azure Storage Explorer:
http://storageexplorer.com

## New Images feature
https://docs.microsoft.com/en-us/azure/virtual-machines/linux/capture-image
```
az image create -g admin_resources -n ubuntu_gpu_image1
--source "https://adminlsmlhse645221.blob.core.windows.net/images/ubuntugpu.vhd"
--os-type linux
```

Can share images across subscription:
```
/subscriptions/<subscriptionId>/resourceGroups/admin_resources/providers/Microsoft.Compute/images/ubuntu_gpu_image1
```

## Managed disk resize (including OS disk)
https://docs.microsoft.com/en-us/azure/virtual-machines/linux/expand-disks

## Copy VHD images accross storage accounts (obsolete, use managed disks and images)
All images are copied to students' storage accounts with
`python generate_azcopy_commands.py` and running the resulting
`azcopy.bat` on Windows VM in Azure.

##  Mounting data disks
You can mount data disks with `./mount_disk.sh`.

## Create image from VM
Save all needed user files from home directory to /usr/local/backup, the user will be deleted.
  
Capture machine: https://docs.microsoft.com/en-us/azure/virtual-machines/virtual-machines-linux-capture-image

Azure CLI 2.0 commands for capturing:
```
Over SSH: sudo waagent -deprovision+user
az vm deallocate -g admin_resources -n ubuntugpu
az vm generalize -g admin_resources -n ubuntugpu
az vm capture -g admin_resources -n ubuntugpu --vhd-name-prefix ubuntugpu
```

## NC6 vs NV6 machine

Both work with NC6 image on Ubuntu 16.04.
Approx. same price.
M60 has less but faster cores and new architecture: 
https://www.quora.com/What-are-the-major-differences-between-the-Nvidia-Tesla-M60-and-K80

| Parameter     | NC6 (K80)     | NV6 (M60)    |
| ------------- |:-------------:|:------------:|
| ConvNet       | 14min 41s     | 8min 41s     |
| Memory        | 12GB          | 8GB          |


## On new ubuntu 14.04 machine
```
sudo apt-get update
sudo apt-get install language-pack-en
```

## HDP 2.5 cluster setup

Installation guide: http://docs.hortonworks.com/HDPDocuments/Ambari-2.4.2.0/bk_ambari-installation/content/download_the_ambari_repo_ubuntu14.html
Disable THP: 
```
sudo bash
echo never >/sys/kernel/mm/transparent_hugepage/enabled
```
Use cluster[1-3] nodes names.
Change `dfs.namenode.datanode.registration.ip-hostname-check` in `hdfs-site.xml`.


