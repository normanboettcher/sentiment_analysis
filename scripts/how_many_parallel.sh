#!/bin/bash

# 1. CPU-Threads bestimmen
THREADS=$(lscpu | grep "Thread(s) per core:" | awk '{print $4}')
CORES=$(lscpu | grep "Core(s) per socket:" | awk '{print $4}')
SOCKETS=$(lscpu | grep "Socket(s):" | awk '{print $2}')
LOGICAL_CPUS=$((THREADS * CORES * SOCKETS))

echo "Gefundene logische CPUs (Threads): $LOGICAL_CPUS"

# 2. Optimale Parallelität berechnen
PARALLEL_JOBS=$((LOGICAL_CPUS * 2))

echo "Possible parallele Jobs: $PARALLEL_JOBS"