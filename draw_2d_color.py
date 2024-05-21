from pathlib import Path

import numpy             as np
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
import os
from matplotlib import colormaps as cm

from hilbert import decode

num_dims = 2

def draw_curve( num_bits, file_path):
  # Path to the .exe file
  # file_path = 'vs.exe'

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
  image = Image.new('RGB', (side_length, side_length))
  pixels = image.load()

  # Normalize the padded array values to [0, 1] for colormap
  normalized_values = padded_array / 255.0

  # Get a colormap (e.g., 'viridis')
  colormap = plt.cm.viridis

  # Map the normalized values to RGB colors using the colormap
  colors = (colormap(normalized_values)[:, :3] * 255).astype(np.uint8)

  # Map the values to the image
  for i, (x, y) in enumerate(coords):
    pixels[x, y] = tuple(colors[i])

  # Save the image
  image.save(file_path+'.png')


def get_files_in_directory(directory):
  files = []
  # Create a Path object for the directory
  directory_path = Path(directory)
  # Iterate through all files in the directory
  for file in directory_path.iterdir():
    # Check if the current file is a regular file
    if file.is_file():
      files.append(file.name)
  return files

def list_files_with_paths(directory):
  file_paths = [str(file) for file in Path(directory).rglob('*') if file.is_file()]
  return file_paths

if __name__ == '__main__':
  exe_files = get_files_in_directory('F:\DATA\COURS UVBF\MEMOIRE\DikeDataset-main\DikeDataset-main\\files\malware')
  i = 0
  total_files = len(exe_files)
  for exe_file in exe_files:
    i+=1
    print(i, '/', total_files, '-------->', exe_file)
    draw_curve(8, exe_file)

