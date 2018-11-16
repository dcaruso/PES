#!/bin/bash
echo "Setup Influx and grafana"
systemctl start influxd &
echo "Starting influxd"
sleep 4
echo "Drop old databases"
influx -execute 'drop database test'
sleep 2
echo "Create database"
influx -execute 'CREATE DATABASE test'

echo "Starting grafana server"
service grafana-server start &
