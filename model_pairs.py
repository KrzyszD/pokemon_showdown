import numpy as np

import torch
import torch.utils
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.autograd import Function


class NeuralNetPairs(torch.nn.Module):
    def __init__(self, lrate):
        """
        Initialize the layers of your neural network
        @param lrate: The learning rate for the model.
        """
        super(NeuralNetPairs, self).__init__()

        self.relu = nn.ReLU(inplace=True)
        self.sigmoid = nn.Sigmoid()
        
        self.fc1 = nn.Linear(979, 50)
#         self.fc2 = nn.Linear(50, 50)
        self.fc3 = nn.Linear(50, 1)
        
        
        self.optimizer = optim.SGD(self.get_parameters(), lrate, momentum=0.1,
                                   weight_decay=1e-3)

        self.loss_fn = nn.MSELoss(reduction='sum')

    def get_parameters(self):
        """ Get the parameters of your network
        @return params: a list of tensors containing all parameters of the network
        """
        return self.parameters()


    def forward(self, x):
        """ A forward pass of your autoencoder
        
        @param x: a batch of (N, 898) torch tensor
        
        @return x: a batch of (N, 1) torch tensor
        
        """

        x = self.fc1(x)
        x = self.relu(x)

#         x = self.fc2(x)
#         x = self.relu(x)

        x = self.fc3(x)
        x = self.sigmoid(x)
        
        return x

    def step(self, x, y):
        """
        Performs one gradient step through a batch of data x with labels y
        @param x: an (N, 979) torch tensor
        @param y: an (N, ) torch tensor
        
        @return L: total empirical risk (mean of losses) at this time step as a float
        """
        
        pred = self.forward(x)
        
        loss = self.loss_fn(pred, y)
    
        self.optimizer.zero_grad()
    
        loss.backward()
    
        self.optimizer.step()
    
        L = loss.item()
    
        return L
        