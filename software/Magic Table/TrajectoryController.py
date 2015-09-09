import time

class TrajectoryController(object):
    # def __init__(self, machine, calibration, trajectory):
    #     pass
    pass

    @staticmethod
    def followTrajectory(points, machine, limits, delay=0.1):
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

