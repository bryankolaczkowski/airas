#!/bin/zsh

for et in all res ins del;
do
  for fx in True False;
  do
    ./calcBalProbReport.py ${et} ${fx} > BalProbReports/IntFixed.${et}.${fx}.csv
    echo "done ${et} ${fx}"
  done
done

echo "finished"
