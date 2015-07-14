#!/usr/bin/python

import pandas
import pickle

# Read in the data file
traits = pandas.read_csv("../tsv/cattell_personality_282.tsv",sep="\t")
pickle.dump(traits,open("../pickle/cattell_personality_282.pkl","wb"))
traits.to_json("../json/cattell_personality_282.json",orient="records")
