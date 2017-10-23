"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  Note for CIS 322 Fall 2016:
#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    # Check for control dist > brevet dist (must round first) and adjust accordingly
    # moved from flask-brevet for testing purposes
    control_dist_km = int(control_dist_km + .5)
    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km
    
    # Calculate time offset in minutes (can be 0)
    max_speeds = [(600,28),(400,30),(200,32),(0,34)]
    time = 0
    for i in range(len(max_speeds)):
        distance, speed = max_speeds[i]
        while control_dist_km > distance:
            time += 60/speed
            control_dist_km -= 1
    
    # ACP rules require round to nearest minute
    time = round(time)
    
    # Store offset time then return as json object
    open_time = brevet_start_time.shift(minutes=+time)
    return open_time.for_json()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
    # Check for control dist > brevet dist (must round first) and adjust accordingly
    # moved from flask-brevet for testing purposes
    control_dist_km = int(control_dist_km + .5)
    if control_dist_km > brevet_dist_km:
        control_dist_km = brevet_dist_km
    
    time = 0
    max_times = [(200,13.5),(300,20),(400,27),(600,40),(1000,75)]
    min_speed = [(600,11.428),(0,15)]
    
    # If control is final check point then special end time stored in max_times
    if control_dist_km == brevet_dist_km:
        for i in range(len(max_times)):
            dist, m_time = max_times[i]
            if brevet_dist_km == dist:
                time = m_time*60
    
    # Else calculate time in minutes based on distance traveled
    else:
        for j in range(len(min_speed)):
            dist, speed = min_speed[j]
            while control_dist_km > dist:
                time += 60/speed
                control_dist_km -= 1
        
        # Round per ACP rules
        time = round(time)
        
        # If time is 0, then at the start, add 1hr
        if time == 0:
            time = 60
    
    # Store offset time then return as json object
    close_time = brevet_start_time.shift(minutes=+time)
    return close_time.for_json()

