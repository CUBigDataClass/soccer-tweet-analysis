#!/bin/bash

source ../config_teams.sh

#run each team
for TEAM in $TEAM_HASHTAGS
do
  echo "Collecting for" $TEAM
  /opt/spark/bin/spark-submit get_tweets.py $TEAM
done
