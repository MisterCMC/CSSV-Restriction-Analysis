from sys import argv
from count import Count
from count import Species
from count import Enzyme
import random
import numpy as np
script, site_file = argv



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
enzyme_range = 6
enzyme_min = 5

quality = 0
data = np.zeros( (len(enzyme_list), enzyme_range) )
for j in range(0, enzyme_range):
    n = j + enzyme_min
    quality = 0
    for enzyme in enzyme_list:
        enzymes[enzyme].reset_points()
    for i in range(0, 100000):
        if i % 1000 == 0:
            print(str(n) + ': '+ str(i))
        enzyme_set = create_enzymes(enzyme_list, True, n)
        find_profiles(species_list, enzyme_set)
        identical_species = compare_profiles(species_list)
        quality = len(identical_species) - len(species_list)
        for enzyme in enzyme_set:
            enzymes[enzyme].set_points(quality)
    for i in range(0, len(enzyme_list)):
        current_enzyme = enzyme_list[i]
        data[i][j] = enzymes[current_enzyme].get_points()

output = open('Enzyme_data.txt', 'w')
output.truncate()
for i in range(0, len(enzyme_list)):
    output.write(enzyme_list[i])
    output.write(', ')
    for j in range(0, enzyme_range):
        output.write(str(data[i][j]))
        output.write(',')
    output.write('\n')
output.close()
