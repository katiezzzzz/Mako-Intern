import testSampleData
import numpy as np

def main():
    x = testSampleData.testSampleData(1000)
    x.insertValue(1, 1000, 2000, 5000)
    x.insertValue(2, 1100, 2100, 6000)
    x.insertValue(3, 1200, 2200, 7000)
    x.insertValue(4, 1300, 2500, 8000)
    x.insertValue(5, 1400, 2600, 9000)
    y = x.getActualData()
    myStdDev = np.std(y.corrPrices)


    print('blah')


if __name__ == '__main__':
    main()