#!/bin/bash

dir="$PWD"
echo "Current Working Directory:$dir"

function usage {
	echo "Provide the path to directory containing "
	echo "narrowPeak output from MACS2"
	
}

if [ $# -ne 1 ]; then
	usage "Path to directory containing MACS2 output:"
	exit 2
fi

NARROW_PEAK=$1

cd $NARROW_PEAK
for file in *.narrowPeak;do cp -r --backup=t "$file" "$file.bed";done
mkdir narrowPeak
mv *narrowPeak.bed narrowPeak

cd narrowPeak
ls *.bed> list.beds
split -l 1 list.beds list.beds.1way

for g in list.beds.1waya?; do echo $g; for file in $(cat $g); do echo ${file}; e=$(echo ${file}| cut -f1 -d"."); echo $e;   bedtools merge -i ${file} -d 12500 > $e.merged.bed ; done & done

cat *.bed > UNION_ALL.bed
sort -k1,1 -k2,2n UNION_ALL.bed | bedtools merge -i stdin -d 0 > UNION_ALL_merged.bed

