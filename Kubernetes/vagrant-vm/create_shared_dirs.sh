#! /usr/bin/bash

mkdir share
mkdir share/master
cp ../auto-installation/*.* ./share/master/.

for i in {1..3}; do
   mkdir ./share/node$i
   cp ../auto-installation/*.* ./share/node$i/.
done
