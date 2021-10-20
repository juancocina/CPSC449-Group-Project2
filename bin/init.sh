#!/bin/bash

sqlite-utils insert ./var/users.db users --csv ./share/users.csv --detect-types --pk=id
sqlite-utils create-index ./var/users.db id username bio email password --unique

sqlite-utils insert ./var/users.db followers --csv ./share/followers.csv --detect-types --pk=id
sqlite-utils create-index ./var/users.db followers id follower_id following_id --unique

