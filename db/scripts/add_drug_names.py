import numpy as np
import pickle
import psycopg2
import requests
import sys
import time

from typing import List


def get_all_treatments():
    treatments = []
    try:
        # TODO add these as env vars
        connection = psycopg2.connect(user="",
                                      password="",
                                      host="df-treats-db.cs6hxh6ocizm.us-west-2.rds.amazonaws.com",
                                      port="5432",
                                      database="")
        cursor = connection.cursor()
        query = "SELECT id, name from treatments"
        cursor.execute(query)
        treatments = [(drug[0], drug[1]) for drug in cursor.fetchall()]
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        cursor.close()
        connection.close()
    return treatments


def update_rxnorm_ids(treatments: List[str], local_group: int):
    # list of tuple(id, drug_name)
    rxnorm_ids = {}
    for treatment in treatments:
        not_found = True
        if not treatment[1]:
            continue
        treat = treatment[1].lower()
        # strip trademark
        treat = treat.replace(u"\u2122", '')
        # strip drug combination
        treat = treat.replace("drug combination", '')
        # split by commas and/or spaces
        treat = treat.replace(' ', ',')
        split_treats = treat.split(',')
        # TODO add original treatment name in with spaces subbed with regex for space
        for split_treat in split_treats:
            split_treat = split_treat.strip()
            # too lazy to actually fix
            if not split_treat:
                continue
            # prevent going over api limit
            time.sleep(1)
            r = requests.get(f'https://rxnav.nlm.nih.gov/REST/rxcui.json?name={split_treat}')
            if r.status_code == 200:
                try:
                    rxnorm_id = r.json()['idGroup']['rxnormId']
                    l = rxnorm_ids.get(treatment, [])
                    l.extend(rxnorm_id)
                    rxnorm_ids[treatment] = l
                    print(f"found id for {treatment}")
                    not_found = False
                except Exception as e:
                    print(e)
                    continue
            elif r.status_code == 403:
                print(f"throttled API with group {local_group}")
                raise Exception
            else:
                print(f"Status code{r.status_code} for treat {split_treat}")
        if not_found:
            print(f"did not find id for {treatment}")
    file_name = f'local_rxnorm_ids_{local_group}.pkl'
    print(f"writing to {file_name}")
    with open(file_name, 'wb') as f:
        pickle.dump(rxnorm_ids, f)


def get_brand_names(rxnorm_id: str):
    time.sleep(1)
    r = requests.get(f'https://rxnav.nlm.nih.gov/REST/rxcui/{rxnorm_id[0]}/allrelated.json')
    if r.status_code != 200:
        print("ugh")
        return

    concept_groups = r.json()['allRelatedGroup']['conceptGroup']
    brand_names = []
    for concept_group in concept_groups:
        if concept_group.get('tty', '') == 'BN':
            if 'conceptProperties' in concept_group:
                brand_names_dict = concept_group['conceptProperties']
                for brand_name in brand_names_dict:
                    brand_names.append(brand_name['name'])
            break
    print(f"Found brand names {brand_names}")
    return brand_names


if __name__ == '__main__':
    command = sys.argv[1]

    if command == "update_local_treatments":
        # split into 20 groups to run at same time within rate limit
        all_treats = np.array_split(get_all_treatments(), 20)
        for i in range(20):
            with open(f'local_treats_{i}.pkl', 'wb') as f:
                curr_treats = all_treats[i].tolist()
                curr_treats = [tuple(curr_treats) for curr_treats in curr_treats]
                pickle.dump(curr_treats, f)

    if command == "update_rxnorm_id":
        group = int(sys.argv[2])
        with open(f'local_treats_{group}.pkl', 'rb') as f:
            data = pickle.load(f)
            update_rxnorm_ids(data, group)

    if command == "update_drug_names":
        group = int(sys.argv[2])
        drug_to_brand_names = {}
        with open(f'local_rxnorm_ids_{group}.pkl', 'rb') as f:
            data = pickle.load(f)
            for t in data:
                norm_ids = data[t]
                names = get_brand_names(norm_ids)
                if len(names) > 0:
                    drug_to_brand_names[t] = names
        file_name = f'local_drug_to_brand_names_{group}.pkl'
        print(f"writing to {file_name}")
        with open(file_name, 'wb') as f:
            pickle.dump(drug_to_brand_names, f)

    if command == "write_drug_names":
        treats_to_brand_names = {}
        for i in range(20):
            with open(f'local_drug_to_brand_names_{i}.pkl', 'rb') as f:
                data = pickle.load(f)
                treats_to_brand_names.update(data)
        count = 0
        for t in treats_to_brand_names:
            brand_names = treats_to_brand_names[t]
            if len(brand_names) >= 1:
                if t[1] in brand_names:
                    if len(brand_names) > 1:
                        count += 1
                else:
                    print(t)
                    print(brand_names)
                    count += 1
        print(count)
