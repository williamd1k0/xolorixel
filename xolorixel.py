"""
MIT License

Copyright (c) 2017 William Tumeo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import sys
from PIL import Image
import yaml

def load_palettes(path):
    return yaml.load(open(path, 'r', encoding='utf-8'))

def load_image(path):
    return Image.open(path).convert('RGB')


def write_images(input_path, palettes, base_name):
    count = 0
    template = os.path.join(
        os.path.dirname(input_path), base_name[0]+'.{n}'+base_name[1]
    )
    for pal in palettes['output']:
        print('Palette:', pal)
        img = load_image(input_path)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if list(pixels[x, y]) in palettes['input']:
                    index = palettes['input'].index(list(pixels[x, y]))
                    pixels[x, y] = tuple(pal[index])
                else:
                    print('WARN: Wrong color/palette ' + str(pixels[x, y]))
        print('Image saved:', template.format(n=count))
        img.save(template.format(n=count))
        count += 1
        del img


def main(args):
    # Temp sys args
    input_file = os.path.abspath(args[0])
    palettes = load_palettes(args[1])
    write_images(input_file, palettes, os.path.splitext(input_file))

if __name__ == '__main__':
    main(sys.argv[1:])

