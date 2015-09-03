from xml.dom.minidom import parseString
from svg.path import parse_path
from math import ceil

__author__ = 'def'

class Trajectory:
    def __init__(self):
        self.paths = []

    @staticmethod
    def _extract_paths_from_svg(svg_filepath):
        path_strings = []

        # Load file contents
        svg_contents = None
        with open(svg_filepath, 'r') as f:
            svg_contents = f.read()

        # Parse xml
        dom = parseString(svg_contents)

        # Find all "path" nodes
        for path_node in dom.getElementsByTagName("path"):
            try:
                path_str = path_node.getAttribute('d')
                if path_str:
                    path_strings.append(path_str)
            except (IndexError, AttributeError) as e:
                pass

        return path_strings

    def load_paths_from_svg(self, svg_filepath):
        path_strings = self._extract_paths_from_svg(svg_filepath)
        self.paths = [ parse_path(path_str) for path_str in path_strings]

    def get_path(self, path_index, starting_point_index=0, step=1):
        path = self.paths[path_index]
        ordered_path = path[starting_point_index:] + path[0:starting_point_index]
        return self._discretize(ordered_path, step)

    def get_normalized_path(self, path_index, starting_point_index=0, step=1):
        """Step is applied before normalizing"""
        discrete_path = self.get_path(path_index, starting_point_index, step)
        bounding_box = self._bounding_box(discrete_path)
        return self._scale(discrete_path, 1/float(bounding_box[1][0]-bounding_box[0][0]),
                                          1/float(bounding_box[1][1]-bounding_box[0][1]))

    # Path transformations
    @staticmethod
    def _discretize(path, segment_len):
        points = []
        for element in path:
            samples = int(ceil(element.length() / segment_len))
            for i in range(samples):
                num = element.point(i/samples)
                points.append( (num.real, num.imag))
        return points

    @staticmethod
    def _scale(discrete_path, scale_factor_x, scale_factor_y):
        return [(p[0]*scale_factor_x, p[1]*scale_factor_y) for p in discrete_path]

    @staticmethod
    def _translate(discrete_path, x_translate, y_translate):
        return [(p[0]+x_translate, p[1]+y_translate) for p in discrete_path]

    @staticmethod
    def _bounding_box(discrete_path):
        min_x = min(x for x, y in discrete_path)
        max_x = max(x for x, y in discrete_path)
        min_y = min(y for x, y in discrete_path)
        max_y = max(y for x, y in discrete_path)
        return [(min_x, min_y), (max_x, max_y)]

