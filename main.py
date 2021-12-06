# Hamming code(7,4)
import numpy as np


def encode_hamming(message):
    """
    Encodes a 4 bit message with three parity bits. Hamming(7,4)
    :param message: Binary message of length 4 passed as numpy array
    :return: returns the 7 bit encoded message to transmit
    """
    assert len(message) == 4 and type(message) == np.ndarray, \
        "Message has incompatible length or wrong type"
    generator = np.array([[1, 1, 0, 1],
                          [1, 0, 1, 1],
                          [1, 0, 0, 0],
                          [0, 1, 1, 1],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 0, 1]])
    return np.dot(generator, message) % 2


def parity_check(transmit_message):
    """
    Checks 7 bit hamming code for 1-bit errors
    :param transmit_message: a 4-4 bit message ecoded to a 7-bit hamming liner code
    :return: If there are errors in transmission, returns syndrome vector
    """
    assert len(transmit_message) == 7 and type(transmit_message) == np.ndarray, \
        "Message has incompatible length or wrong type"
    H = np.array([[1, 0, 1, 0, 1, 0, 1],
                  [0, 1, 1, 0, 0, 1, 1],
                  [0, 0, 0, 1, 1, 1, 1]])
    syndrome_vector = np.dot(H, transmit_message) % 2
    if sum(syndrome_vector) == 0:
        return "No 1-bit errors"
    else:
        enum_syndrome = np.array([i for i, bit in enumerate(syndrome_vector) if syndrome_vector[i] == 1])
        syndrome_index = np.power(2, enum_syndrome)  # Binary product of syndrome vector gives index for error
        syndrome_index = sum(syndrome_index) - 1  # Remove 1 for the all zero vector which is not an alternative
        return print("1-bit error found at index", syndrome_index, "\n", "Syndrome vector", syndrome_vector)


def decode_hamming(transmit_message):
    """
    Takes a 7-bit encoded hemming (7,4) and returns the original message.
    :param transmit_message: 7-bit encoded Hemming code
    :return: Original message
    """
    assert len(transmit_message) == 7 and type(transmit_message) == np.ndarray, \
        "Message has incompatible length or  wrong type"
    R = np.array([[0, 0, 1, 0, 0, 0, 0],
                               [0, 0, 0, 0, 1, 0, 0],
                               [0, 0, 0, 0, 0, 1, 0],
                               [0, 0, 0, 0, 0, 0, 1]])
    return np.dot(R, transmit_message)


# Test parity check function
real_message = np.array([1, 1, 1, 1])
real_message = encode_hamming(real_message)
print(real_message)
edited_message = np.array([1, 1, 0, 1, 1, 1, 1])
parity_check(edited_message)  # Should give error message of 1-bit error found at index 3


# Unit test for encode and decode functions, test assumes working parity check
def unit_test():
    for i in range(16):
        x = np.random.randint(0, 2, 4)
        y = encode_hamming(x)
        a = parity_check(y)
        if type(a) != str:  # If encoding is wrong, return input and output value of encode_hamming
            print(x)
            print(a)
        # Test decode_hamming
        z = decode_hamming(y)
        if not np.array_equal(z, x):
            return print(z, " not equal to ", x)

    print("Unit test complete: no errors found")


# # unit_test()
# mes = np.array([1, 0, 1, 0])
# print(mes)
# b = encode_hamming(mes)
# print(b)
# print(decode_hamming(b))
