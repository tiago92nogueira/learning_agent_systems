import numpy as np
import json

class NeuralNet:

    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        self.w1 = np.random.randn(input_size, hidden_size)
        self.b1 = np.zeros((1, hidden_size))
        
        self.w2 = np.random.randn(hidden_size, output_size)
        self.b2 = np.zeros((1, output_size))

    def forward(self, x):
       
        x = np.array(x).reshape(1, -1)
        
        self.z1 = np.dot(x, self.w1) + self.b1
        self.a1 = np.tanh(self.z1)
        
        self.z2 = np.dot(self.a1, self.w2) + self.b2
        output = self.z2
        
        return output.flatten()

    def get_weights(self):
        return np.concatenate((
            self.w1.flatten(), 
            self.b1.flatten(), 
            self.w2.flatten(), 
            self.b2.flatten()
        ))

    def set_weights(self, flat_weights):
       
        w1_end = self.input_size * self.hidden_size
        b1_end = w1_end + self.hidden_size
        w2_end = b1_end + (self.hidden_size * self.output_size)
        
        self.w1 = flat_weights[:w1_end].reshape(self.input_size, self.hidden_size)
        self.b1 = flat_weights[w1_end:b1_end].reshape(1, self.hidden_size)
        self.w2 = flat_weights[b1_end:w2_end].reshape(self.hidden_size, self.output_size)
        self.b2 = flat_weights[w2_end:].reshape(1, self.output_size)

    def save_to_file(self, filename):
        data = {
            "input_size": self.input_size,
            "hidden_size": self.hidden_size,
            "output_size": self.output_size,
            "weights": self.get_weights().tolist()
        }
        with open(filename, 'w') as f:
            json.dump(data, f)

    @staticmethod
    def load_from_file(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        
        net = NeuralNet(data["input_size"], data["hidden_size"], data["output_size"])
        net.set_weights(np.array(data["weights"]))
        return net