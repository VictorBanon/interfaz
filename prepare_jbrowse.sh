#!/usr/bin/env bash
set -euo pipefail

# Usage: ./prepare_jbrowse.sh file.fa myfile.gff
# Requires: samtools, bgzip, tabix, npm, jbrowse-cli

FASTA="$1"
GFF="$2"

# Check dependencies
# command -v samtools >/dev/null 2>&1 || { echo "samtools not found. Install samtools."; exit 1; }
# command -v bgzip >/dev/null 2>&1 || { echo "bgzip not found. Install htslib."; exit 1; }
# command -v tabix >/dev/null 2>&1 || { echo "tabix not found. Install htslib."; exit 1; }
# command -v jbrowse >/dev/null 2>&1 || { echo "jbrowse not found. Run: npm install -g @jbrowse/cli"; exit 1; }

# Step 1: Prepare FASTA index
echo "Indexing FASTA..."
bgzip -c "$FASTA" > "${FASTA}.gz"
samtools faidx "${FASTA}.gz"

# Step 2: Prepare GFF3 for JBrowse
echo "Sorting and indexing GFF3..."
SORTED_GFF="${GFF%.gff}.sorted.gff"
(sort -k1,1 -k4,4n "$GFF") > "$SORTED_GFF"

bgzip -c "$SORTED_GFF" > "${SORTED_GFF}.gz"
tabix -p gff "${SORTED_GFF}.gz"

echo "All done!"
echo "Generated files:"
echo " - ${FASTA}.gz and ${FASTA}.gz.fai"
echo " - ${SORTED_GFF}.gz and ${SORTED_GFF}.gz.tbi"
