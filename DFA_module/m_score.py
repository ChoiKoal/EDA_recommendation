import numpy as np
import scipy.stats
import scipy.spatial
import random
import math
import sys
import csv
import pandas as pd
from collections import Counter, defaultdict

class MatchPerformance():
    def __init__(self, data_dict, combination_dict, scenario_dict):
        self.data_dict = data_dict
        self.combination_dict = combination_dict
        self.scenario_dict = scenario_dict