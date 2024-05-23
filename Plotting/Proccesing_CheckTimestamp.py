# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 07:45:43 2024

@author: jeppe
"""

from AirmasterDataLib import loadData

import datetime
import matplotlib.pyplot as plt
data = loadData.load_data("C:/Users/jeppe/OneDrive - Aalborg Universitet/8. Semester Shared work/data-2/data-2/404000113/404000113.pkl")
teledata=loadData.load_telemetry()
X=loadData.extract_sensor_data(data, "rqf")
for i in X["timestamps"]:
    print(i)
    print(datetime.datetime.fromtimestamp(i))
fig, ax = plt.subplots(1,1)
loadData.plot_sensor_data(ax,X, "rqf")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

