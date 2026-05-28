#!/bin/bash
# Batch download script for trading strategy research
# Downloads missing data for 44 symbols across 4 timeframes

cd /c/Users/danyw/Documents/Git/DanywayGit/BacktestingMCP
source venv/Scripts/activate

LOG="/c/Users/danyw/Documents/Git/DanywayGit/BacktestingMCP/download_log.txt"
echo "=== Batch Download Started $(date) ===" > "$LOG"

run_dl() {
    local sym="$1" tf="$2" start="$3"
    echo "Downloading $sym $tf from $start ..." | tee -a "$LOG"
    python -m src.cli.main data download --symbol "$sym" --timeframe "$tf" --start "$start" --end 2024-12-31 2>&1 | tail -3 | tee -a "$LOG"
    if [ ${PIPESTATUS[0]} -ne 0 ]; then
        echo "FAILED: $sym $tf $start" | tee -a "$LOG"
    else
        echo "OK: $sym $tf $start" | tee -a "$LOG"
    fi
}

echo "=== Group 1: Missing 15m for symbols that already have 12h/4h/1h ===" | tee -a "$LOG"
# Established - 15m from 2022-01-01
for sym in "BTC/USDT" "ETH/USDT" "SOL/USDT" "SHIB/USDT" "NEAR/USDT" "DOGE/USDT" "BNB/USDT" "ADA/USDT" "LINK/USDT" "BCH/USDT" "FIL/USDT" "INJ/USDT" "AVAX/USDT" "UNI/USDT" "DOT/USDT" "LTC/USDT" "TRX/USDT" "ICP/USDT"; do
    run_dl "$sym" "15m" "2022-01-01"
done

# Mid-age - APT from 2022-10-19, OP from 2022-06-01
run_dl "APT/USDT" "15m" "2022-10-19"
run_dl "OP/USDT" "15m" "2022-06-01"

# ARB - 15m from 2023-03-23
run_dl "ARB/USDT" "15m" "2023-03-23"

# SEI - 15m from 2023-08-15
run_dl "SEI/USDT" "15m" "2023-08-15"

echo "=== Group 2: Symbols with only 15m/1h in DB - need 12h, 4h, 1h ===" | tee -a "$LOG"
# AAVE, ATOM, DASH - established coins
for sym in "AAVE/USDT" "ATOM/USDT" "DASH/USDT"; do
    run_dl "$sym" "12h" "2021-01-01"
    run_dl "$sym" "4h"  "2021-01-01"
    run_dl "$sym" "1h"  "2021-01-01"
    run_dl "$sym" "15m" "2022-01-01"
done

# ALGO, SAND - established coins
for sym in "ALGO/USDT" "SAND/USDT"; do
    run_dl "$sym" "12h" "2021-01-01"
    run_dl "$sym" "4h"  "2021-01-01"
    run_dl "$sym" "1h"  "2021-01-01"
    run_dl "$sym" "15m" "2022-01-01"
done

# ETC - established
run_dl "ETC/USDT" "12h" "2021-01-01"
run_dl "ETC/USDT" "4h"  "2021-01-01"
run_dl "ETC/USDT" "1h"  "2021-01-01"
run_dl "ETC/USDT" "15m" "2022-01-01"

# DYDX - try from 2022
run_dl "DYDX/USDT" "12h" "2022-01-01"
run_dl "DYDX/USDT" "4h"  "2022-01-01"
run_dl "DYDX/USDT" "1h"  "2022-01-01"
run_dl "DYDX/USDT" "15m" "2022-01-01"

# SUI - newer, try from 2023
run_dl "SUI/USDT" "12h" "2023-01-01"
run_dl "SUI/USDT" "4h"  "2023-01-01"
run_dl "SUI/USDT" "1h"  "2023-01-01"
run_dl "SUI/USDT" "15m" "2023-01-01"

echo "=== Group 3: Completely missing symbols ===" | tee -a "$LOG"
# POL - mid-age
for tf in "1h" "4h" "12h" "15m"; do
    run_dl "POL/USDT" "$tf" "2022-01-01"
done

# FET - mid-age
for tf in "1h" "4h" "12h" "15m"; do
    run_dl "FET/USDT" "$tf" "2022-01-01"
done

# RENDER - newer
for tf in "1h" "4h" "12h" "15m"; do
    run_dl "RENDER/USDT" "$tf" "2023-01-01"
done

# CHZ - established
for tf in "1h" "4h" "12h" "15m"; do
    run_dl "CHZ/USDT" "$tf" "2021-01-01"
done

# MANA, FLOW, AXS, RUNE - established
for sym in "MANA/USDT" "FLOW/USDT" "AXS/USDT" "RUNE/USDT"; do
    run_dl "$sym" "1h"  "2021-01-01"
    run_dl "$sym" "4h"  "2021-01-01"
    run_dl "$sym" "12h" "2021-01-01"
    run_dl "$sym" "15m" "2022-01-01"
done

# GMX - mid-age (launched ~2021-09)
for tf in "1h" "4h" "12h" "15m"; do
    run_dl "GMX/USDT" "$tf" "2022-01-01"
done

echo "=== Group 4: Very new tokens - attempt downloads ===" | tee -a "$LOG"
# HYPE - very new, likely only 2025
run_dl "HYPE/USDT" "15m" "2024-01-01"
run_dl "HYPE/USDT" "1h"  "2024-01-01"

# ONDO - new
run_dl "ONDO/USDT" "15m" "2023-01-01"
run_dl "ONDO/USDT" "1h"  "2023-01-01"

# TON - newer
run_dl "TON/USDT" "15m" "2023-01-01"
run_dl "TON/USDT" "1h"  "2023-01-01"

# TAO - newer
run_dl "TAO/USDT" "15m" "2023-01-01"
run_dl "TAO/USDT" "1h"  "2023-01-01"

# ENA - 2024
run_dl "ENA/USDT" "15m" "2024-01-01"
run_dl "ENA/USDT" "1h"  "2024-01-01"

echo "=== All downloads complete $(date) ===" | tee -a "$LOG"
