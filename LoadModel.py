import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression

def loadModel(fn):
    nclass = 163
##    network = input_data(shape=[None, 55, 55,1], name='input')
##    network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
##    network = max_pool_2d(network, 2)
##    network = local_response_normalization(network)
##    network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
##    network = max_pool_2d(network, 2)
##    network = local_response_normalization(network)
##    network = conv_2d(network, 128, 3, activation='relu', regularizer="L2")
##    network = max_pool_2d(network, 2)
##    network = local_response_normalization(network)
##    network = fully_connected(network, 256, activation='tanh')
##    network = dropout(network, 0.8)
##    network = fully_connected(network, 512, activation='tanh')
##    network = dropout(network, 0.8)
##    network = fully_connected(network, nclass, activation='softmax')
##    network = regression(network, optimizer='SGD', learning_rate=0.01,
##                         loss='categorical_crossentropy', name='target')

    network = input_data(shape=[None, 55, 55,1], name='input')
    network = conv_2d(network, 32, 3, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = local_response_normalization(network)
    network = conv_2d(network, 64, 3, activation='relu', regularizer="L2")
    network = max_pool_2d(network, 2)
    network = local_response_normalization(network)
    ##network = conv_2d(network, 128, 3, activation='relu', regularizer="L2")
    ##network = max_pool_2d(network, 2)
    ##network = local_response_normalization(network)
    network = fully_connected(network, 128, activation='tanh')
    network = dropout(network, 0.8)
    network = fully_connected(network, 256, activation='tanh')
    network = dropout(network, 0.8)
    network = fully_connected(network, nclass, activation='softmax')
    network = regression(network, optimizer='SGD', learning_rate=0.01,
                         loss='categorical_crossentropy', name='target')
    
    model = tflearn.DNN(network, tensorboard_verbose=0)
    model.load(fn)
    return model
