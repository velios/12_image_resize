from argparse import ArgumentParser
from os import path
import logging
from math import isclose

from PIL import Image


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def make_cmd_arguments_parser():
    parser_description = 'Script resize original image'
    parser = ArgumentParser(description=parser_description,
                            add_help=False)
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


def resize_image(image, desired_width, desired_height, desired_scale):
    original_width, original_height = image.size
    if not any((desired_scale, desired_width, desired_height)):
        raise ValueError('Not enough arguments for resize image')
    elif desired_scale and (desired_width or desired_height):
        raise ValueError('You can\'t simultaneously enter the scale and length or height')
    elif desired_scale:
        result_width = original_width * desired_scale
        result_height = original_height * desired_scale
    else:
        result_width = desired_width if desired_width else\
            original_width * desired_height / original_height
        result_height = desired_height if desired_height else\
            original_height * desired_width / original_width
    result_width, result_height = round(result_width), round(result_height)
    return image.resize((result_width, result_height))


def check_proportions(original_width, original_height, result_width, result_height):
    return isclose(
        original_width / original_height,
        result_width / result_height,
        rel_tol=0.01,
    )


if __name__ == '__main__':
    cmd_arguments = make_cmd_arguments_parser()
    original_file_path, input_width, input_height, input_scale, output_file_path = (cmd_arguments.original,
                                                                                    cmd_arguments.width,
                                                                                    cmd_arguments.height,
                                                                                    cmd_arguments.scale,
                                                                                    cmd_arguments.output,)
    try:
        original_image = Image.open(original_file_path)
        original_file_name, original_file_extension = path.splitext(path.basename(original_file_path))
        original_width, original_height = original_image.size
        result_image = resize_image(
            image=original_image,
            desired_scale=input_scale,
            desired_height=input_height,
            desired_width=input_width,
        )
        result_width, result_height = result_image.size
        if not output_file_path:
            output_file_path = '{}__{}x{}{}'.format(
                original_file_name,
                result_width,
                result_height,
                original_file_extension
            )
        if not check_proportions(original_width=original_width, original_height=original_height,
                                 result_width=result_width, result_height=result_height):
            print('The proportions do not match the original image')
        result_image.save('{}{}'.format(output_file_path, original_file_extension))
        print('Result save to file {}'.format(output_file_path))
    except (ValueError, FileNotFoundError) as err:
        print('Cmd arguments error:', err)
