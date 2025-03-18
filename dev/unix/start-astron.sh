#!/bin/sh
cd ../../lib/astron

while [ true ]
do
  ./astrond-linux --loglevel info config/astrond.yml
done
