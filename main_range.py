from sys import argv
from count import Count
from count import Species
from count import Enzyme
import random
import numpy as np
script, site_file = argv

data = np.zeros( (1000, 36) )

in_file = open(site_file).read()
in_file_list = in_file.split('\n')
site_list = []
for i in range(0, len(in_file_list)):
    site_list.append(in_file_list[i].split('\t'))

def create_list(in_list, type):
    data_list = []
    for i in range(0, len(in_list)-1):
        site = in_list[i]
        if site[type] in data_list:
            continue
        elif site[type] not in data_list:
            data_list.append(site[type])
    return data_list

def create_object(in_list, type):
    object_dct = {}
    for i in range(0, len(in_list)):
        object_dct[in_list[i]] = type(in_list[i])
    return object_dct

def count_sites(in_list, type, object):
    for i in range(0, len(in_list)-1):
        site = in_list[i]
        object[site[type]].set_count()

def find_restriction(in_list):
    for i in range(0, len(in_list)-1):
        site = in_list[i]
        species[site[0]].set_restriction(site[1])

def create_enzymes(full_list, rand, length):
    if rand == False:
        return full_list
    if rand == True:
        n = random.sample(range(0, len(full_list)), length)
        rand_enzymes = []
        for i in range(0, len(n)):
            rand_enzymes.append(full_list[n[i]])
        return rand_enzymes

def find_profiles(species_list, enzyme_list):
    for i in range(0, len(species_list)):
        species[species_list[i]].reset_profile()
        sites = species[species_list[i]].get_restriction()
        for j in range(0, len(enzyme_list)):
            if enzyme_list[j] in sites:
                species[species_list[i]].set_profile(True)
            elif enzyme_list[j] not in sites:
                species[species_list[i]].set_profile(False)

def compare_profiles(species_list):
    identicals = []
    for i in range(0, len(species_list)):
        if species_list[i] in identicals:
            continue
        current_profile = species[species_list[i]].get_profile()
        identical_species = [species_list[i]]

        for j in range(i+1, len(species_list)):
            checked_profile = species[species_list[j]].get_profile()
            if current_profile != checked_profile:
                continue
            elif current_profile == checked_profile:
                identical_species.append(species_list[j])

        for j in range(0, len(identical_species)):
            identicals.append(identical_species[j])
        identicals.append('\n')
    return identicals


# create lists and objects
enzyme_list = create_list(site_list, 1)
enzymes = create_object(enzyme_list, Enzyme)

species_list = create_list(site_list, 0)
species = create_object(species_list, Species)

# count sites and define restriction sites
count_sites(site_list, 1, enzymes)
count_sites(site_list, 0, species)
find_restriction(site_list)

# main loop
best = 0
best_list = []
best_enzymes = []
best_enzymes_list = []
quality = 0

for j in range(1, 36):
    print(j)
    best = 0
    best_enzymes = []
    quality = 0
    for i in range(0, 1000):
        enzyme_set = create_enzymes(enzyme_list, True, j)
        find_profiles(species_list, enzyme_set)
        identical_species = compare_profiles(species_list)
        quality = len(identical_species) - len(species_list)
        data[i][j] = quality

        if quality > best:
            best = quality
            best_enzymes  = enzyme_set
            profiles = identical_species

    best_enzymes_list.append(best_enzymes)
    best_list.append(best)

print(best_list)
print(best_enzymes_list)
output = open('Enzyme_range_data.txt', 'w')
output.truncate()
for i in range(1, 1000):
    for j in range(1, 36):
        output.write(str(data[i][j]))
        output.write(',')
    output.write('\n')
output.close()
