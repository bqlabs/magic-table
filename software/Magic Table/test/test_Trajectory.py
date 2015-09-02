import unittest
import os
from Trajectory import Trajectory
from svg.path import Path, Line

__author__ = 'def'


class TrajectoryTest(unittest.TestCase):

    svg_filepath = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data', 'test_python.svg')
    scaled_svg_filepath = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'data', 'test_scaled_python.svg')

    def test_extract_paths_from_svg(self):
        traj = Trajectory()
        path_strings = traj._extract_paths_from_svg(self.svg_filepath)
        self.assertEqual(len(path_strings), 2)
        self.assertEqual(path_strings[0], "M 99.75,67.46875 C 71.718268,67.468752 73.46875,79.625 73.46875,79.625 L 73.5,92.21875 L 100.25,92.21875 L 100.25,96 L 62.875,96 C 62.875,96 44.9375,93.965724 44.9375,122.25 C 44.937498,150.53427 60.59375,149.53125 60.59375,149.53125 L 69.9375,149.53125 L 69.9375,136.40625 C 69.9375,136.40625 69.433848,120.75 85.34375,120.75 C 101.25365,120.75 111.875,120.75 111.875,120.75 C 111.875,120.75 126.78125,120.99096 126.78125,106.34375 C 126.78125,91.696544 126.78125,82.125 126.78125,82.125 C 126.78125,82.124998 129.04443,67.46875 99.75,67.46875 z M 85,75.9375 C 87.661429,75.937498 89.8125,78.088571 89.8125,80.75 C 89.812502,83.411429 87.661429,85.5625 85,85.5625 C 82.338571,85.562502 80.1875,83.411429 80.1875,80.75 C 80.187498,78.088571 82.338571,75.9375 85,75.9375 z ")
        self.assertEqual(path_strings[1], "M 100.5461,177.31485 C 128.57784,177.31485 126.82735,165.1586 126.82735,165.1586 L 126.7961,152.56485 L 100.0461,152.56485 L 100.0461,148.7836 L 137.4211,148.7836 C 137.4211,148.7836 155.3586,150.81787 155.3586,122.53359 C 155.35861,94.249323 139.70235,95.252343 139.70235,95.252343 L 130.3586,95.252343 L 130.3586,108.37734 C 130.3586,108.37734 130.86226,124.03359 114.95235,124.03359 C 99.042448,124.03359 88.421098,124.03359 88.421098,124.03359 C 88.421098,124.03359 73.514848,123.79263 73.514848,138.43985 C 73.514848,153.08705 73.514848,162.6586 73.514848,162.6586 C 73.514848,162.6586 71.251668,177.31485 100.5461,177.31485 z M 115.2961,168.8461 C 112.63467,168.8461 110.4836,166.69503 110.4836,164.0336 C 110.4836,161.37217 112.63467,159.2211 115.2961,159.2211 C 117.95753,159.2211 120.1086,161.37217 120.1086,164.0336 C 120.10861,166.69503 117.95753,168.8461 115.2961,168.8461 z " )

    def test_load_paths_from_svg(self):
        traj = Trajectory()
        traj.load_paths_from_svg(self.svg_filepath)
        self.assertEqual(len(traj.paths), 2)

    def test_discretize_path(self):
        traj = Trajectory()
        traj.load_paths_from_svg(self.svg_filepath)
        self.assertEqual(len(traj.paths), 2)

        discrete_traj = traj._discretize(traj.paths[0], 1)
        self.assertEqual(len(discrete_traj), 377)

        for point in discrete_traj:
            self.assertEqual(len(point), 2)

    def test_scale_path(self):
        discrete_traj = [(0,0), (2, 2), (7, 1)]
        discrete_test_traj = [(0,0), (4, 1), (14,0.5)]

        scaled_traj = Trajectory._scale(discrete_traj, 2, 0.5)

        for (x, y) , (test_x, test_y) in zip(scaled_traj, discrete_test_traj):
            self.assertAlmostEqual(x, test_x, delta=0.01)
            self.assertAlmostEqual(y, test_y, delta=0.01)

    def test_translate_path(self):
        discrete_traj = [(0,0), (2, 2), (7, 1)]
        discrete_test_traj = [(3,3.5), (5, 5.5), (10,4.5)]

        translated_traj = Trajectory._translate(discrete_traj, 3, 3.5)

        for (x, y) , (test_x, test_y) in zip(translated_traj, discrete_test_traj):
            self.assertAlmostEqual(x, test_x, delta=0.01)
            self.assertAlmostEqual(y, test_y, delta=0.01)

    def test_bounding_box(self):
        discrete_traj = [(0,0), (2,2), (7,1)]
        test_bounding_box = [(0,0), (7,2)]

        bounding_box = Trajectory._bounding_box(discrete_traj)

        self.assertEqual(bounding_box, test_bounding_box)

    def test_get_path_not_starting_at_0(self):
        test_path = Path(Line(start=(0+0j), end=(2+2j)),
                         Line(start=(2+2j), end=(7+1j)),
                         Line(start=(7+1j), end=(0+0j)))

        expected_result = Trajectory._discretize(Path(Line(start=(2+2j), end=(7+1j)),
                         Line(start=(7+1j), end=(0+0j)), Line(start=(0+0j), end=(2+2j))), 1)

        traj = Trajectory()
        traj.paths.append(test_path)
        result = traj.get_path(0, 1, 1)

        self.assertEqual(result, expected_result)

    def test_get_normalized_path(self):
        self.fail("Test not implemented")