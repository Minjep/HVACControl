
import matplotlib.pyplot as plt
import csv
import pandas
def plotXY(X,Y):
    plt.plot(X,Y)
    plt.title('Position')
    plt.xlabel('Longitude (m)')
    plt.ylabel('Latitude (m)')
    plt.grid()
    plt.show()

def loadFile(file):
    csvFile = pandas.read_csv(file)
    return csvFile


csvFile = loadFile("kalmanFFirst.csv")
print(csvFile)
plotXY(csvFile.iloc[:,0],csvFile.iloc[:,1])

