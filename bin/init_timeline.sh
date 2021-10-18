#!/bin/bash

sqlite-utils insert ./var/timeline.db timelines --csv ./share/timeline.csv --detect-types --pk=id
sqlite-utils create-index ./var/timeline.db