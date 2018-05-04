#!/bin/bash

dir="$PWD"
echo "Current Working Directory:$dir"

function usage {
	echo "Provide the path to directory containing "
	echo "bed files and UNION_ALL_merged.bed"
	
}

if [ $# -ne 1 ]; then
	usage "Path to directory containing MACS2 output:"
	exit 2
fi

COVERAGE=$1

cd $COVERAGE

ls *.bed > list.beds

split -l 1 list.beds list.beds.1way

for g in list.beds.1waya?; do echo $g; \
for file in $(cat $g); do echo ${file}; e=$(echo ${file}| cut -f1 -d"."); \
echo $e;   bedtools coverage -a UNION_ALL_merged_wo_TSS.bed -b ${file} -counts  > $e.reads.bed ; done & done
