import time
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.linear_model import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils import check_random_state
import pickle


# Load data from https://www.openml.org/d/554
suffix = "2"
X = np.load(f"backup/X{suffix}.npy")
# base = 3 * 200
# X = X[:,base:base+200]
y = np.load(f"backup/y{suffix}.npy")
print("X")
print(type(X))
print(X.shape)
print("y")
print(type(y))
print(y.shape)
train_samples = len(y)

# Turn up tolerance for faster convergence
clf = LogisticRegression(C=50.0 / train_samples, penalty="l2", solver="liblinear", tol=0.01)

def train(clf):
    global X, y

    t0 = time.time()

    random_state = check_random_state(0)
    permutation = random_state.permutation(X.shape[0])
    X = X[permutation]
    y = y[permutation]
    X = X.reshape((X.shape[0], -1))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, train_size=None, test_size=None
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    clf.fit(X_train, y_train)

    run_time = time.time() - t0
    print("Train in %.3f s" % run_time)

    return (clf, X_test, y_test)

def evaluate(clf, X_test, y_test):
    global X, y

    t0 = time.time()

    sparsity = np.mean(clf.coef_ == 0) * 100
    score = clf.score(X_test, y_test)
#   print('Best C % .4f' % clf.C_)
    print("Sparsity with L1 penalty: %.2f%%" % sparsity)
    print("Test score with L1 penalty: %.4f" % score)

    run_time = time.time() - t0
    print("Predict in %.3f s" % run_time)

    return score

print(f"{np.mean([evaluate(*train(clf)) for _ in range(100)])=}")

with open("fmodel{suffix}.pkl", "wb") as f:
    pickle.dump(train(clf)[0], f)
