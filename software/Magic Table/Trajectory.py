from xml.dom.minidom import parseString
from svg.path import parse_path

__author__ = 'def'

class Trajectory:

    class TrajectoryException(BaseException):
        pass

    def __init__(self):
        self.paths = None

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