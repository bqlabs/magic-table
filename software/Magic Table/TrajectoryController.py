import time
from threading import Lock

class TrajectoryController(object):

    def __init__(self):
        self.lock = Lock()
        self.stop = False

    def askToStop(self):
        self.lock.acquire()
        self.stop = True
        self.lock.release()

    def followTrajectory(self, points, machine, limits, delay=0.1):
        # Reset flag
        self.lock.acquire()
        self.stop = False
        self.lock.release()

        # Get limits points
        try:
            upperLeft = limits['upper_left_limit']
            lowerRight = limits['lower_right_limit']
        except (AttributeError, KeyError) as e:
            print str(e)
            return False

        width_working_area = lowerRight[1] - upperLeft[1]
        height_working_area = lowerRight[0] - upperLeft[0]

        # Map points
        real_points = []
        for x, y in points:
            real_points.append((y*height_working_area+upperLeft[1],
                                 x*width_working_area+upperLeft[0]))

        print "Go to: "
        print real_points

        # Move machine
        for x, y in real_points:
            try:
                machine.move(x, y)
            except AttributeError, e:
                print "Out of limits"
                print e
            time.sleep(delay)

            # Test if stop was requested
            self.lock.acquire()
            if self.stop:
                self.lock.release()
                return False
            self.lock.release()

        return True
