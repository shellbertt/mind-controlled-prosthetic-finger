import numpy as np

def info(X, y):
    print(f"{type(X)}=")
    print(f"{X.shape=}")
    print(f"{type(y)=}")
    print(f"{y.shape=}")

def load(X_name, y_name):
    X = np.load(X_name)
    y = np.load(y_name)
    info(X, y)
    return (X, y)

a, b, c = "new", "3", "upto3"
X1, y1 = load(f"X{a}.npy", f"y{a}.npy")
X2, y2 = load(f"X{b}.npy", f"y{b}.npy")
Xnew = np.concat((X1, X2))
ynew = np.concat((y1, y2))
info(Xnew, ynew)
np.save(f"X{c}", Xnew)
np.save(f"y{c}", ynew)
