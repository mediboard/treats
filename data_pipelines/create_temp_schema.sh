#!/bin/bash

# Dump the schema for the meditreats database
pg_dump -U meditreats -F p -s meditreats > meditreats_schema.sql

# Check if the temp_schema exists and drop it if it does
EXISTS=$(psql -U meditreats -tAc "SELECT 1 FROM pg_namespace WHERE nspname = 'temp_schema'")
if [ "$EXISTS" == "1" ]; then
  psql -U meditreats -c "DROP SCHEMA temp_schema CASCADE"
fi

# Replace the name of the schema in the dump file
perl -pi -e 's/public/temp_schema/g' meditreats_schema.sql

# Load the modified dump file into the database
psql -U meditreats < meditreats_schema.sql
