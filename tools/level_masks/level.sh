#!/bin/bash

## used to create thumbnails of every levels (max:6) on a bounty page

function info() {
    echo "$0 TravelPoint_Mode_Num.png LEVELS
    TravelPoint : 'The Barrens', 'Felwood', ... or 'Onyxia'
    Mode : 'Normal' or 'Heroic'
    Num : page '1' or '2' or '3'

    LEVELS : how many levels are in the level page (4 or 6 ?)

    Info : will create 4 or 6 files based on masks"
    exit 1
}

[ $# -eq 2 ] || info

FILE="$1"
NAME=${FILE%%.png}

LEVELS="$2"
for((i=1; i<=$LEVELS;i++)); do
    convert "$FILE" \( level_mask${LEVELS}_${i}.png -alpha off -negate \) -compose copy_opacity  -composite -trim "${NAME}${i}.png"
done
