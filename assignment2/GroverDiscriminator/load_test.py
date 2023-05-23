import numpy

import pandas as pd

data = numpy.load('test-probs.npy')
pd.DataFrame(data).to_csv('prob.csv')

