#!/usr/bin/env python3

import argparse
from itertools import cycle
import pickle
import json

"""
    Describes the heat-map to apply to the points.
    keys -- can be in any unit, as long as the same unit is used for picking the color
    colors -- list of (R,G,B) tuples, to apply to the relevant keys
    clip -- list (R,G,B) tuples of the clipping color if point is outside of range, [<min, >max], if None it's ignored
"""
color_gradient = {
    "keys": [0, 2000, 4000],
    "colors": [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
    ],
    "clip": [
        None,
        (0, 0, 0)
    ]
}

parser = argparse.ArgumentParser(description='Processes data.pickle files from the AAU picoflex robot platform')
parser.add_argument('-i', '--increments', dest='increments',
                    default=50,
                    help='Distance to move linearly between images [mm]')
parser.add_argument('file',
                    help='Path to the data.pickle file to use')
parser.add_argument('-o', '--output_directory',
                    help='The folder to put the generated depth maps in')

#args = parser.parse_args()


# Arduino map function
def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def lerp(x, l_color, u_color):
    """
    Get a linear interpolated color between to colors
    :param x: position between colors to interpolate. 0.0-1.0 float
    :param l_color: Lower bound of the colors to mix. (R,G,B) tuple
    :param u_color: Upper bound of the colors to mix. (R,G,B) tuple
    :return: Linear interpolated color between l_color and u_color. (R,G,B) tuple
    """
    out_color = (
        l_color[0] * x + u_color[0] * x,
        l_color[1] * x + u_color[1] * x,
        l_color[2] * x + u_color[2] * x
    )

    return out_color


def get_color(distance):
    """
    Get a color for a given distance, according to the color_gradient
    :param distance: Distance of the point, in the same unit as the color_gradient keys
    :return: (R, G, B) tuple
    """

    """Clips to min clip color if provided"""
    if color_gradient['clip'][0] is not None and distance < color_gradient['keys'][0]:
        return color_gradient['clip'][0]

    """Clips to max clip color if provided"""
    if color_gradient['clip'][1] is not None and distance > color_gradient['keys'][-1]:
        return color_gradient['clip'][1]

    for idx, key in enumerate(color_gradient['keys']):
        if idx == 0:
            continue

        if distance < key:
            relative_distance = map_range(
                distance,
                color_gradient['keys'][idx-1],
                color_gradient['keys'][idx],
                0.0,
                1.0
            )
            return lerp(relative_distance, color_gradient['colors'][idx-1], color_gradient['colors'][idx])


print(get_color(1000))

