# COMP9021 Term 3 2019


'''
Produces ascii art from a picture.
'''


from argparse import ArgumentParser
from re import sub
from statistics import mean
from itertools import count
from math import ceil
import os

from PIL import Image


parser = ArgumentParser()
parser.add_argument('--image_file', dest='image_filename', required=True)
parser.add_argument('--alphabet', dest='alphabet', required=False)
parser.add_argument('--nb_of_pixels', dest='nb_of_pixels', required=False)
args = parser.parse_args()
image_filename = args.image_filename
try:
    # Record the luminance of each pixel.
    image = Image.open(image_filename).convert('L')
except FileNotFoundError:
    print(f'File {image_filename} could not be found.')
except OSError:
    print(f'File {image_filename} could not be processed as an image file.')
# Each ascii character will be put at the centre of a box of size
# 2.5mm x 2.5mm. We want the ascii picture to be of maximum size
# 80 * 2.5mm x 100 * 2.5mm = 200mm x 250mm.
min_nb_of_pixels = max(ceil(image.size[0] / 80), ceil(image.size[1] / 100))
try:
    nb_of_pixels = max(int(args.nb_of_pixels), min_nb_of_pixels)
except TypeError:
    nb_of_pixels = min_nb_of_pixels
width = image.size[0] // nb_of_pixels
height = image.size[1] // nb_of_pixels
# We will crop the image symetrically if needed.
x_offset = image.size[0] % nb_of_pixels // 2
y_offset = image.size[1] % nb_of_pixels // 2
# A string of ascii characters to replace pixels,
# from darkest to brightest.
alphabet = args.alphabet
if not alphabet:
    alphabet = '@%#*+=-:. '
image_name = sub('\..*', '', image_filename)
ascii_image_name = image_name + '_ascii'
if os.path.isfile(ascii_image_name + '.tex'):
    for i in count():
        ascii_image_name = image_name + '_ascii_' + str(i)
        if not os.path.isfile(ascii_image_name + '.tex'):
            break
tex_filename = ascii_image_name + '.tex'
pixels = tuple(image.getdata())
max_luminance = max(pixels)
min_luminance = min(pixels)
luminance_range = max_luminance - min_luminance + 1
with open(tex_filename, 'w') as tex_file:
    print('\\documentclass[10pt]{article}\n'
          '\\usepackage{fancyvrb}'
          # As we want to be able to output any ascii character, we do
          # not choose an ascii character for that surrounding
          # character; we (arbitrarily) choose the character obtained
          # on a Mac by pressing Option 0.
          '\\DefineShortVerb{\\º}\n'
          '\\usepackage{tikz}\n'
          '\\usepackage[margin=0cm]{geometry}\n'
          '\\pagestyle{empty}\n'
          '\n'
          '\\begin{document}\n'
          '\n'
          '\\vspace*{\\fill}\n'
          '\\begin{center}\n'
          '\\begin{tikzpicture}[x=2.5mm, y=-2.5mm]', file=tex_file
         )
    for i in range(height):
        y = y_offset + i * nb_of_pixels
        for j in range(width):
            x = x_offset + j * nb_of_pixels
            node_luminance = alphabet[
                    int((mean(tuple(image.crop((x, y, x + nb_of_pixels,
                                                y + nb_of_pixels
                                               )
                                              ).getdata()
                                   )
                             ) - min_luminance
                        ) / luminance_range * len(alphabet)
                       )
                                     ]
            # Note the use of {{ and }} to output { and }, respectively.
            print(f'\\node at ({j}, {i}) {{º{node_luminance}º}};',
                  file=tex_file
                 )
    print('\\end{tikzpicture}\n'
          '\\end{center}\n'
          '\\vspace*{\\fill}\n\n'
          '\\end{document}', file = tex_file
         )
os.system('lualatex ' + tex_filename)
for file in (ascii_image_name + ext for ext in ('.aux', '.log')):
    os.remove(file)
print(f'\nProduced {ascii_image_name + ".pdf"}, replacing blocks of '
      f'{nb_of_pixels}x{nb_of_pixels} pixels by one character.'
     )
