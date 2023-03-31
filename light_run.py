#run
from acknowledge.acknowledge import few_shot, instruction
from acknowledge.completions import *

import pandas as pd
import pickle
import numpy as np
import json

path_to_file='your-path'
df_sample = pd.read_csv(path_to_file)
print(df_sample.shape)

few_shot(df_sample, 'Funding Text', checkpoint_name='your_checkpoint_name', model='gpt-3.5-turbo')