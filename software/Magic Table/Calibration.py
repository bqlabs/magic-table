import os
import zipfile
from xml.dom.minidom import parseString

__author__ = 'def'


class Calibration:
    def __init__(self):
        self.xmlcontents = None
        self.points = []
        self.image_name = None
        self.image = None

        self.calibrating = False
        self.real_points = []

    # Data loading members
    # --------------------------------------------------------------------------
    class LoadException(ValueError):
        pass

    def load_zipfile(self, path):
        with zipfile.ZipFile(path, 'r') as zfile:
            # Check if file is correct
            if 'calibration.xml' not in  zfile.namelist():
                raise Calibration.LoadException("Incorrect calibration file")

            # Load main xml file
            with zfile.open('calibration.xml', 'rU') as xmlfile:
                self.xmlcontents = xmlfile.read()

            self._parse_xml()

            # Load image if necessary
            if self.image_name:
                if self.image_name in zfile.namelist():
                    with zfile.open(self.image_name, 'r') as imagefile:
                        self.image = imagefile.read()
                else:
                    raise Calibration.LoadException("Incorrect calibration file (could not load image)")

    def _parse_xml(self):
        if not self.xmlcontents:
            raise Calibration.LoadException('Could not load xml data')

        dom = parseString(self.xmlcontents)

        # Get image (if found)
        try:
            image_node = dom.getElementsByTagName("image")[0]
            try:
                image_name_node = image_node.getElementsByTagName("name")[0]
                image_name_text_node = image_name_node.childNodes[0]
                if image_name_text_node.nodeType == image_name_text_node.TEXT_NODE:
                    self.image_name = image_name_text_node.data
                else:
                    raise Calibration.LoadException("Image name was not a string")
            except (IndexError, AttributeError) as e:
                raise Calibration.LoadException("Incorrect calibration file (%s)" % str(e))
        except IndexError:
            pass

        # Get calibration points
        point_nodes = dom.getElementsByTagName("point")
        for point_node in point_nodes:
            try:
                point = {}
                # Get name
                point_name_node = point_node.getElementsByTagName("name")[0]
                point_name_text_node = point_name_node.childNodes[0]
                if point_name_text_node.nodeType == point_name_text_node.TEXT_NODE:
                    point['name'] = point_name_text_node.data
                else:
                    raise

                # Get symbol
                point_symbol_node = point_node.getElementsByTagName("name")[0]
                point_symbol_text_node = point_symbol_node.childNodes[0]
                if point_symbol_text_node.nodeType == point_symbol_text_node.TEXT_NODE:
                    point['symbol'] = point_symbol_text_node.data
                else:
                    raise

                # Get point coordinates
                point_coordinates_node = point_node.getElementsByTagName("coordinates")[0]
                point['coordinates'] = (float(point_coordinates_node.getAttribute('x')), float(point_coordinates_node.getAttribute('y')))

                # Add point
                self.points.append(point)

            except (IndexError, AttributeError) as e:
                print str(e)
                continue

    # Calibration methods stuff
    # ---------------------------------------------------------------------------------------
    def start(self):
        """ Starts the calibration process """
        pass

    def abort(self):
        """ Stops a calibration process """
        pass

    def set_current_point_pos(self, point):
        """ Sets the x,y values for the current point """
        pass

    def get_current_point_data(self, point):

        pass

    def next(self):
        """
        Go to next calibration point.
        :return: None if there is no point left
        """
        pass

    def get_calibration_xml(self):
        pass


if __name__ == '__main__':
    calibration = Calibration()
    zfile = calibration.load_zipfile(os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources',
                             'calibration', 'calibration.zip')))

    assert calibration.xmlcontents, 'File not loaded'
    assert calibration.points, 'Points not loaded'
    print calibration.points
    assert calibration.image_name, 'Image path not loaded'
    assert calibration.image, 'Image not loaded'