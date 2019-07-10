# import main
import json
import sys
import os
import pytest

sys.path.append(os.path.abspath('src'))

try:
    MODULE = os.path.dirname(os.path.realpath('main.py'))
except:
    MODULE = ""

import main

sys.path.append(MODULE)

LawAnalyzer = main.LawAnalyzer


def test_law():
    la = LawAnalyzer(r"src/test/data/testing_law_2.json")
    d = la.load_corpus()
    with open(r"src/test/data/relations.json") as fd:
        rel = json.load(fd)
    for k, v in rel.items():
        results = la.query(k)
        arts = set(x[1] for x in results)
        pytest.assume(arts == set(v), f'Correct: {v}, Answer: {arts}')
