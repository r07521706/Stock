import math
import datetime
from tabulate import tabulate
from wave_info.deal_with_wave import *
from wave_logic.wave_logic_function import *
from matplotlib import pyplot as plt
from FinMind.Data import Load
import numpy as np
import json
import pandas as pd


TaiwanStockInfo = Load.FinData(dataset = 'TaiwanStockInfo')
rs=test1(8088)

print(tabulate(rs[0], headers='keys', tablefmt='psql'))
rs[0].to_csv("earn.csv")
print(tabulate(rs[1], headers='keys', tablefmt='psql'))
rs[1].to_csv("lose.csv")
