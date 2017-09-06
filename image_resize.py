from argparse import ArgumentParser
from os import path

from PIL import Image


def make_cmd_arguments_parser():
    parser_description = 'Script resize original image'
    parser = ArgumentParser(description=parser_description, add_help=False)
    parser.add_argument('original',
                        help='path to original image',
                        type=str)
    parser.add_argument('--width', '-w',
                        help='width of result image',
                        type=int)
    parser.add_argument('--height', '-h',
                        help='height of result image',
                        type=int)
    parser.add_argument('--scale', '-s',
                        help='scale for resize result image',
                        type=float)
    parser.add_argument('--output', '-o',
                        help='name of result file without extension')
    parser.add_argument('--help', action='help', default='==SUPPRESS==',
                        help='show this help message and exit')
    return parser.parse_args()


def resize_image(path_to_original, path_to_result=None, desired_scale=1, desired_width=None, desired_height=None):
    original_filename, original_fileextension = path.splitext(path.basename(path_to_original))
    image = Image.open(original_file)
    original_width, original_heigth = image.size
    if not any((desired_scale, desired_width, desired_height)):
        raise ValueError('Not enough arguments for resize image')
    elif desired_scale and (desired_width or desired_height):
        raise ValueError('You can\'t simultaneously enter the scale and length or height')
    elif desired_scale:
        result_width = original_width * desired_scale
        result_height = original_heigth * desired_scale
    else:
        result_width = desired_width if desired_width else original_width * desired_height / original_heigth
        result_height = desired_height if desired_height else original_heigth * desired_width / original_width
    if original_width / result_width != original_heigth / result_height:
        print('Notice:', 'The proportions do not match the original image')
    result_width, result_height = round(result_width), round(result_height)
    if path_to_result:
        output_filepath = ''.join((path_to_result, original_fileextension))
    else:
        output_filepath = '{}__{}x{}{}'.format(original_filename, result_width,
                                               result_height, original_fileextension)
    image.resize((result_width, result_height)).save(output_filepath)
    print('Result save to file {}'.format(output_filepath))


if __name__ == '__main__':
    cmd_arguments = make_cmd_arguments_parser()
    original_file, input_width, input_height, input_scale, output_file = (cmd_arguments.original,
                                                                          cmd_arguments.width,
                                                                          cmd_arguments.height,
                                                                          cmd_arguments.scale,
                                                                          cmd_arguments.output)
    try:
        resize_image(path_to_original=original_file, path_to_result=output_file,
                     desired_scale=input_scale, desired_height=input_height, desired_width=input_width)
    except ValueError as err:
        print('Cmd arguments error:', err)
