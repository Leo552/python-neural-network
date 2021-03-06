import numpy as np
import numba_neural_network as nn
import z_helper as h
import time
np.set_printoptions(linewidth=200)

data_input = np.load("data/ci_inputs.npy")
data_output = np.load("data/ci_outputs.npy")

print(data_input.shape)
print(data_output.shape)

print("Begin compiling!")
begin_time = time.time_ns()
compiled_nn_values = nn.make_neural_network(layer_sizes=[data_input.shape[1], data_output.shape[1]], layer_activations=[h.softmax])
nn.train_auto(data_input[:100], data_output[:100], data_input[100: 140], data_output[100: 140], compiled_nn_values)
end_time = time.time_ns()
print("Compile time:", (end_time-begin_time) / 1e9)

np.random.seed(420)
total_accuracy = 0.0
begin_total = time.time_ns()
n = 10
for i in range(n):

    random_seed = np.random.randint(10, 1010)
    np.random.seed(random_seed)

    train_input, validate_input, test_input = h.kfold(7, data_input, random_seed)
    train_output, validate_output, test_output = h.kfold(7, data_output, random_seed)

    nn_values = nn.make_neural_network(layer_sizes=[train_input.shape[1], 20, train_output.shape[1]], layer_activations=[h.sigmoid, h.softmax])

    begin_time = time.time_ns()
    epochs, current_mse = nn.train_auto(train_input, train_output, validate_input, validate_output, nn_values)
    end_time = time.time_ns()

    train_mse = nn.calculate_MSE(train_input, train_output, nn_values)
    test_mse = nn.calculate_MSE(test_input, test_output, nn_values)

    accuracy_test = nn.evaluate(test_input, test_output, nn_values)
    total_accuracy += accuracy_test
    print("Seed:", random_seed, "Epochs:", epochs, "Time:", (end_time-begin_time)/1e9, "Accuracy:", accuracy_test, "Tr:", train_mse, "V:", current_mse, "T:", test_mse)
print("Average Accuracy:", total_accuracy / n, "Average Time:", ((time.time_ns()-begin_total)/1e9) / n)
