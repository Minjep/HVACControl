import numpy as np


def simModel(xR:np.array,xV:np.array,u:np.array,recirc:bool):
    AR = np.array([[810.5, 8.8], [48.0, 879.8]]) * 1e-3
    BR = np.array([[-1.2, -0.1, -0.2, 0.0, -1.1, -2.2],
                [0.5, 0.1, 1.3, -0.1, 0.9, 1.8]]) * 1e-3
    CR = np.array([[-60.7, -1.8],
                [-2711.0, -3222.3]])
    AV = np.array([[913.3, -78.6], [288.0, 144.6]]) * 1e-3
    BV = np.array([[-0.7, -0.3, 0.3, -0.2, -5.5, -5.2],
                [1.5, 0.3, -0.1, -0.8, 31.6, -0.9]]) * 1e-3
    CV = np.array([[-31.3, 0.4],
                [-1141.8, 755.0]])
    
    
    xk1R=AR.dot(xR)+BR.dot(u)
    yR=CR.dot(xV)

    xk1V=AV.dot(xV)+BV.dot(u)
    yV=CV.dot(xV)

    
    if recirc==True:
        return xk1R,xk1V,yR
    else:
        return xk1R,xk1V,yV

    




if __name__ == "__main__":
    X_recirc=np.array([[0,0],[0,0]])
    X_vent=np.array([[0,0],[0,0]])
    Y=np.array([[0],[0]])
    for i in range(0,10):
        U = np.random.rand(6, 1)

        X_recirc,X_vent,Y=simModel(X_recirc,X_vent,U,True)