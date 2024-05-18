import numpy             as np
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
from matplotlib import colormaps as cm

from hilbert import decode

num_dims = 2

def draw_curve( num_bits):
  # Path to the .exe file
  file_path = 'vs.exe'

  # Read the .exe file in binary mode
  with open(file_path, 'rb') as file:
    binary_data = file.read()

  # Convert the binary data to a numpy array
  # dtype=np.uint8 to represent the binary data as unsigned 8-bit integers
  numpy_array = np.frombuffer(binary_data, dtype=np.uint8)

  # The maximum Hilbert integer.
  max_h = 2**(num_bits*num_dims)

  # Determine the dimensionality and order of the Hilbert curve
  dims = 2  # for a 2D Hilbert curve
  bits = int(np.ceil(np.log2(len(numpy_array) ** (1 / dims))))  # Number of bits needed

  # Reshape the array to fit the Hilbert curve requirements
  side_length = 2 ** bits
  padded_size = side_length ** dims
  padded_array = np.pad(numpy_array, (0, padded_size - len(numpy_array)), mode='constant')

  # Convert the padded array to coordinates on the Hilbert curve
  coords = decode(np.arange(padded_size), dims, bits)

  # Create an empty image
  image = Image.new('L', (side_length, side_length))
  pixels = image.load()

  # Map the values to the image
  for i, (x, y) in enumerate(coords):
    pixels[x, y] = int(padded_array[i])

  # Save the image
  image.save('hilbert_curve_image_vs.png')


draw_curve(8)
