#!/bin/bash

echo "🔍 Analyze system to make a suggestion for parallel HTTP-Requests..."
echo "Output of lscpu will be analyzed based on german output"

# CPU-Cores and Threads
THREADS=$(lscpu | awk '/^Kern\(e\) pro Socket:/ {c=$4} /^Sockel:/ {s=$2} /^Thread\(s\) pro Kern:/ {t=$4} END {print c * s * t}')
CORES=$(lscpu | awk '/^CPU\(s\):/ {print $2}')

echo "🧠  CPU-Cores:        $CORES"
echo "🧵  Logical Threads: $THREADS"

# RAM (frei + verfügbar)
RAM_TOTAL=$(free -m | awk '/Speicher:/ {print $2}')
RAM_FREE=$(free -m | awk '/Speicher:/ {print $7}')
echo "💾  RAM total:       ${RAM_TOTAL} MB"
echo "💤  RAM free:    ${RAM_FREE} MB"

# Offene Dateien / Verbindungen
ULIMIT=$(ulimit -n)
echo "📡  Max. open files (ulimit -n): $ULIMIT"

# Aktuelle Systemlast
LOAD_AVG=$(uptime | awk -F'load average: ' '{print $2}')
echo "📊  current load (1/5/15min): $LOAD_AVG"

# Empfehlung berechnen
RECOMMENDED=$(( THREADS < 50 ? THREADS * 2 : 50 ))

# Anpassung nach RAM
if [ "$RAM_FREE" -lt 1000 ]; then
    RECOMMENDED=$((RECOMMENDED / 2))
    echo "⚠️  Little RAM available → Reduced Recommendation."
fi

# Limit durch ulimit
if [ "$RECOMMENDED" -gt "$ULIMIT" ]; then
    RECOMMENDED=$((ULIMIT - 10))
    echo "⚠️  ulimit is limiting open connections."
fi

# Sicherheitsgrenze
if [ "$RECOMMENDED" -lt 1 ]; then
    RECOMMENDED=1
fi

echo ""
echo "✅ Recommended max. parallelism: $RECOMMENDED parallel HTTP-Requests"
