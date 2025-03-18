#!/bin/sh
cd ../../lib/astron

while [ true ]
do
  ./astrond-darwin --loglevel info config/astrond.yml
done
