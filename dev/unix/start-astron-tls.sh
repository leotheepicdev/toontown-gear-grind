#!/bin/sh
cd ../../lib/astron

while [ true ]
do
  ./astrondlinux --loglevel info config/astrond_tls_dev.yml
done