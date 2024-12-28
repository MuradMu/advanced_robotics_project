import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/murad/advanced_robotics_project/ros2_ws/install/my_test_pkg'
