#!/bin/bash
host=$(kubectl get services | grep "front-end" | grep -Po "NodePort\s*\K(\d+\.\d+\.\d+\.\d+)")
TEST_NAME=load SCRIPT=checkout_client.py HOST=http://$host:80 DURATION=30m USERS=400 RATE=2 WORKERS=8 docker-compose up -d --scale worker=8
