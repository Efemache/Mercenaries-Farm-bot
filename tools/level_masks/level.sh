#!/bin/bash

## used to create thumbnails of every levels (max:6) on a bounty page

function info() {
    echo "$0 TravelPoint_Mode_Num.png
    TravelPoint : 'The Barrens', 'Felwood', ... or 'Onyxia'
    Mode : 'Normal' or 'Heroic'
    Num : page '1' or '2' or '3'

    Info : will create 6 files based on masks"
    exit 1
}

[ $# -eq 1 ] || info

FILE="$1"
NAME=${FILE%%.png}

for((i=1; i<7;i++)); do
    convert "$FILE" \( level_mask_${i}.png -alpha off -negate \) -compose copy_opacity  -composite -trim "${NAME}${i}.png"
done
