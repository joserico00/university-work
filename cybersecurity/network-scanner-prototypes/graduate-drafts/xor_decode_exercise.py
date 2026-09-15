import numpy as np

# Define the array of integers and ensure all values are within the ASCII range using modulo 256
t_values = np.array([
    201, 194, 237, 164, 251, 21, 178, 240, 338, 93, 100, 36, 29, 138, 20, 91, 243, 236, 207, 157, 130, 38, 143, 221, 371, 
    102, 77, 58, 36, 189, 61, 122, 228, 251, 215, 128, 162, 44, 146, 245, 338, 97, 64, 27, 36, 173, 32, 74, 226, 236, 210, 
    154, 157, 25, 128, 219, 352, 100, 68, 29, 36, 187, 18, 117, 199, 224, 211, 140, 182, 40, 141, 197, 337, 102, 77, 0, 34, 
    176, 61, 122, 245, 232, 207, 141, 160, 59, 133, 249, 371, 102, 71, 0, 45, 172
]) % 256
t = ''.join(chr(num) for num in t_values)
print("Initial string t:", t)

# Transformation function applying XOR with a dynamic key
def transform_string(input_string, y):
    result = []
    for char in input_string:
        y = (y * 3) % 0x100 + 6
        result.append(chr(ord(char) ^ y))
    return ''.join(result), y

y = 41
k, y = transform_string(t, y)
print("Registry Path:", k)

# Reset for 'c' calculation
t_values = np.array([154, 205, 142, 177, 19, 230, 201, 218, 109, 6, 88, 242, 211, 47])
t = ''.join(chr(num) for num in t_values)
print("Transformed string t for c:", t)

y = 243
c, y = transform_string(t, y)
print("Registry Key Name:", c)



import pickle
import base64

# The save string you provided
save_string = 'gAN9cQAoWA4AAABMZXZlbENvbXBsZXRlZHEBSwFYBAAAAE5hbWVxAlgGAAAAV2l6YXJkcQNYBgAAAGhlYWx0aHEETV4BWAYAAABhdHRhY2txBU30AXUu'

# Decoding from base64
decoded_data = base64.b64decode(save_string)

# Unpickling the data to see the current values
data = pickle.loads(decoded_data)
print(data)
# Modifying the health and attack values
data['health'] = 1000
data['attack'] = 1000

# Re-pickling the modified data
modified_pickle_data = pickle.dumps(data)

# Encoding the modified pickle data into base64
modified_save_string = base64.b64encode(modified_pickle_data).decode('ascii')
modified_save_string
