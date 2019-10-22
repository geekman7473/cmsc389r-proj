#!/bin/bash

declare -i i=0

while read p; do
    if steghide extract -sf image.jpg -xf out.txt -p $p > /dev/null 2>&1;
    then
        echo "$p is the passphrase!"
        break
    fi

    ((i++))
    if ((i % 10 == 0));
    then
        echo -en "\r$i"
    fi
done <"rockyou.txt"

