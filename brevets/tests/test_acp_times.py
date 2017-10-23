"""
Nose tests for acp_times.py

"""

from acp_times import open_time
from acp_times import close_time

import nose
import arrow
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
log = logging.getLogger(__name__)

TEST_TIME = arrow.get('2017-02-01 22:00:00', 'YYYY-MM-DD HH:mm:ss') #Feb 1, 2017 10pm
BREVET_DISTANCES = [200,300,400,600,1000]
FIN_OPEN_TIMES = [arrow.get('2017-02-02 03:53', 'YYYY-MM-DD HH:mm'),
                  arrow.get('2017-02-02 07:00', 'YYYY-MM-DD HH:mm'),
                  arrow.get('2017-02-02 10:08', 'YYYY-MM-DD HH:mm'),
                  arrow.get('2017-02-02 16:48', 'YYYY-MM-DD HH:mm'),
                  arrow.get('2017-02-03 07:05', 'YYYY-MM-DD HH:mm')]
 
FIN_CLOSE_TIMES = [arrow.get('2017-02-02 11:30', 'YYYY-MM-DD HH:mm'),
                   arrow.get('2017-02-02 18:00', 'YYYY-MM-DD HH:mm'),
                   arrow.get('2017-02-03 01:00', 'YYYY-MM-DD HH:mm'),
                   arrow.get('2017-02-03 14:00', 'YYYY-MM-DD HH:mm'),
                   arrow.get('2017-02-05 01:00', 'YYYY-MM-DD HH:mm')]

MID_OPEN_TIMES = [arrow.get('2017-02-02 00:58', 'YYYY-MM-DD HH:mm'),
                  arrow.get('2017-02-02 03:55', 'YYYY-MM-DD HH:mm'),
                  arrow.get('2017-02-02 07:02', 'YYYY-MM-DD HH:mm'),
                  arrow.get('2017-02-02 13:30', 'YYYY-MM-DD HH:mm'),
                  arrow.get('2017-02-03 03:33', 'YYYY-MM-DD HH:mm')]
 
MID_CLOSE_TIMES = [arrow.get('2017-02-02 04:44', 'YYYY-MM-DD HH:mm'),
                   arrow.get('2017-02-02 11:24', 'YYYY-MM-DD HH:mm'),
                   arrow.get('2017-02-02 18:04', 'YYYY-MM-DD HH:mm'),
                   arrow.get('2017-02-03 07:24', 'YYYY-MM-DD HH:mm'),
                   arrow.get('2017-02-04 16:20', 'YYYY-MM-DD HH:mm')]
 

def test_start_open():
    """
    Start open time (0km) == brevet start time
    """
    for i in range(len(BREVET_DISTANCES)):
        assert open_time(0, BREVET_DISTANCES[i], TEST_TIME) == TEST_TIME.for_json()

def test_start_close():
    """
    Start close time (0km) == brevet start time + 1hr
    """
    for i in range(len(BREVET_DISTANCES)):
        assert close_time(0, BREVET_DISTANCES[i], TEST_TIME) == TEST_TIME.shift(hours=+1).for_json()

def test_finish_open():
    """
    Check the finish opening times, and 20% additional length (max allowed by ACP)
    """
    for i in range(len(BREVET_DISTANCES)):
        assert open_time(BREVET_DISTANCES[i]*1.2, BREVET_DISTANCES[i], TEST_TIME) == \
               FIN_OPEN_TIMES[i].for_json()

def test_finish_close():
    """
    Check the finish closing times, and 20% additional length (max allowed by ACP)
    """
    for i in range(len(BREVET_DISTANCES)):
        assert close_time(BREVET_DISTANCES[i]*1.2, BREVET_DISTANCES[i], TEST_TIME) == \
               FIN_CLOSE_TIMES[i].for_json()

def test_rand_distance():
    """
    not actually random, 98.6 and 99.5 km before end of brevet
    tests for decimals and rounding, as well as intermediate time calculations
    """
    for i in range(len(BREVET_DISTANCES)):
        assert open_time(BREVET_DISTANCES[i]-99.5, BREVET_DISTANCES[i], TEST_TIME) == \
               MID_OPEN_TIMES[i].for_json()
        assert close_time(BREVET_DISTANCES[i]-99.5, BREVET_DISTANCES[i], TEST_TIME) == \
               MID_CLOSE_TIMES[i].for_json()
        assert open_time(BREVET_DISTANCES[i]-98.6, BREVET_DISTANCES[i], TEST_TIME) == \
               MID_OPEN_TIMES[i].for_json()
        assert close_time(BREVET_DISTANCES[i]-98.6, BREVET_DISTANCES[i], TEST_TIME) == \
               MID_CLOSE_TIMES[i].for_json()
