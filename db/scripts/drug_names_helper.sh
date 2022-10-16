#!/bin/sh


# only run 20 at a time to not get IP address blocked
START=0
END=19

#for i in $(eval echo "{$START..$END}")
#do
#	python db/scripts/add_drug_names.py update_rxnorm_id "$i" &
#done

for i in $(eval echo "{$START..$END}")
do
	python db/scripts/add_drug_names.py update_drug_names "$i" &
done

