#!/bin/bash

sqlite-utils insert ./var/users.db users --csv ./share/users.csv --detect-types --pk=id
sqlite-utils create-index ./var/users.db id username bio email password --unique