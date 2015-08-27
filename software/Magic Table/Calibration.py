import os
import zipfile
from xml.dom.minidom import parseString, getDOMImplementation

__author__ = 'def'


class Calibration:
    def __init__(self):
        self.xmlcontents = None
        self.points = []
        self.image_name = None
        self.image = None

        # Calibration-related stuff
        self.calibrating = False
        self.index = None
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
    class CalibrationException(BaseException):
        pass

    def start(self):
        """ Starts the calibration process """
        if not self.calibrating:
            self.calibrating = True
            self.index = 0
            self.real_points = []
        else:
            raise Calibration.CalibrationException("Calibration already started")

    def abort(self):
        """ Stops a calibration process """
        if self.calibrating:
            self.calibrating = False
            self.index = None
            self.real_points = []
        else:
            raise Calibration.CalibrationException("Calibration not started")

    def set_current_point_pos(self, point):
        """ Sets the x,y values for the current point """
        if self.calibrating:
            try:
                self.real_points[self.index] = point
            except IndexError, e:
                self.real_points.append(point)
        else:
            raise Calibration.CalibrationException("Calibration not started")

    def get_current_point_data(self):
        if self.calibrating:
            return self.points[self.index]
        else:
            raise Calibration.CalibrationException("Calibration not started")

    def get_progress(self):
        if self.calibrating:
            return self.index/float(len(self.points))
        else:
            raise Calibration.CalibrationException("Calibration not started")

    def next(self):
        """
        Go to next calibration point.
        :return: None if there is no point left
        """
        if self.calibrating:
            if self.index < len(self.points)-1:
                self.index += 1
                return True
            else:
                self.calibrating = False
                return None
        else:
            raise Calibration.CalibrationException("Calibration not started")

    def get_calibration_xml(self):
        if len(self.points) != len(self.real_points):
            raise Calibration.CalibrationException("Not enough calibration points")

        dom = parseString(self.xmlcontents)
        # impl = getDOMImplementation()

        point_nodes = dom.getElementsByTagName("point")
        for point_node in point_nodes:
            try:
                # Get name
                point_name_node = point_node.getElementsByTagName("name")[0]
                point_name_text_node = point_name_node.childNodes[0]
                if point_name_text_node.nodeType == point_name_text_node.TEXT_NODE:
                    name = point_name_text_node.data
                else:
                    raise

                # Check name and add new node
                for i, point in enumerate(self.points):
                    if point['name'] == name:
                        # Add node
                        realpos_element = dom.createElement('realpos')
                        realpos_element.setAttribute('x', str(self.real_points[i][0]))
                        realpos_element.setAttribute('y', str(self.real_points[i][1]))
                        point_node.appendChild(realpos_element)

            except (IndexError, AttributeError) as e:
                print str(e)
                continue


        return dom.toprettyxml(indent='    ', encoding='utf-8')

    def save_calibration_file(self, filepath):
        xmlcontents = self.get_calibration_xml()
        with open(filepath, 'w') as f:
            f.write(xmlcontents)



if __name__ == '__main__':
    calibration = Calibration()
    zfile = calibration.load_zipfile(os.path.realpath(os.path.join(os.path.dirname(__file__), 'resources',
                             'calibration', 'calibration.zip')))

    assert calibration.xmlcontents, 'File not loaded'
    assert calibration.points, 'Points not loaded'
    print calibration.points
    assert calibration.image_name, 'Image path not loaded'
    assert calibration.image, 'Image not loaded'

    calibration.start()

    watchdog = 0
    while watchdog < 10:
        print "Current point: (%.2f, %.2f)" % calibration.get_current_point_data()['coordinates']
        calibration.set_current_point_pos((100, 100))
        if not calibration.next():
            break
        watchdog +=1
    assert watchdog == 1, 'Calibration went wrong'
    print calibration.real_points

    assert calibration.get_calibration_xml(), 'No xml output'
    print calibration.get_calibration_xml().split('\n')

    calibration.save_calibration_file('calibration.xml')