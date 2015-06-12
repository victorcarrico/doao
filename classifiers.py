import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier

def evaluateKNN(trainData, trainTarget, testData, testTarget):
	kList = [1,3,5,7,10,20,30]#1,3,5,7,10,20,30
	error = 100.0
	best_k = 0
	for k in kList:
		knn = KNeighborsClassifier(n_neighbors = k)
		knn.fit(trainData,trainTarget)
		error_temp = 0.0
		for i in range(len(testData)):
			if (knn.predict(testData[i])[0] != testTarget[i]): error_temp += 1.0
		if(error_temp < error):
			error = error_temp
			best_k = k
	#print "KNN error = %f" %error
	#print "for k = %d" %best_k
	return error, best_k

def random(X,Y):
	z = zip(X,Y)
	np.random.shuffle(z)
	newX, newY = [], []
	for i in z:
		newX.append(i[0])
		newY.append(i[1])
	return newX, newY

def get10Fold_n(X,Y,n):
	#get the n-th fold (of 10 folds) of X,Y as a test set, and all remaining folds as train set.
	testX = getFold(X,n)
	testY = getFold(Y,n)
	trainX = []
	trainY = []
	for i in range(10):
		if (i != n):
			trainX = trainX + getFold(X,i)
			trainY = trainY + getFold(Y,i)
	return trainX, trainY, testX, testY

def getFold(l,n):
	#get the n-th fold (starting from 0, of 10 folds {0,...,9}) from the list l
	return l[n*len(l)/10:(n+1)*len(l)/10]
	 
def KFoldValidation_KNN(X,Y):
	total_error = 0.0
	for i in range(10):
		a,b,c,d = get10Fold_n(X,Y,i)
		error, bestk = evaluateKNN(a,b,c,d )
		print "fold %d:  error:  %f  , best k: %d" %(i+1,error,bestk)
		total_error += error
	total_error = (float(total_error)/len(Y))*100
	print "total error: %f %%" %total_error
	return total_error

def OAOPairList(Y):#getOAOPairList
	#returns OneAgainstOne pairs list, for a given target list 'Y'
	classes = np.unique(Y)
	classes.sort()
	ret = []
	for c1 in classes:
		for c2 in classes:
			if (c1 < c2):
				ret.append((c1,c2))
	return ret

def OAODataSet(X,Y,OAOPair):#getOAODataSet
	#get a sub-dataset only with instance where the target is one from the given in the OAOPair pair
	newX, newY = [], []
	for i in range(len(Y)):
		if ((Y[i] == OAOPair[1]) | (Y[i] == OAOPair[0])):
			newX.append(X[i])
			newY.append(Y[i])
	return newX, newY

def OAOValidation(X,Y):
	pairs = OAOPairList(Y)
	bestError = 100
	bestPair = []
	for p in pairs:
		print "for classes: %d and %d:" %(p[0],p[1])
		nx, ny = OAODataSet(X,Y,p)
		error = KFoldValidation_KNN(nx,ny)
		if (bestError > error):
			bestError = error
			bestPair = p
	print "\nBEST ERROR: %f %% | for class %d vs %d" %(bestError,bestPair[0],bestPair[1])
	return bestError, bestPair


print "-----Avaliando KNN para IRIS - KFOLD-cross validation (10 folds)OAR"
iris = datasets.load_iris()
X, y = iris.data, iris.target
X,y = random(X,y)
KFoldValidation_KNN(X,y)
print "-----Avaliando KNN para IRIS - KFOLD-cross validation (10 folds) OAO"
OAOValidation(X,y)
