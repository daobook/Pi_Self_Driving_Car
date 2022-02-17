# -*- coding: utf-8 -*-
# @Time    : 2017/9/8 11:43
# @Author  : play4fun
# @File    : scan_write_csv.py
# @Software: PyCharm

"""
scan_write_csv.py:把点云写入csv，然后在Sweep Visualizer观看

AZIMUTH方位角，偏振角：
libsweep及其绑定（sweeppy）将方位报告为毫秒的整数，以避免浮点表示而不失去精度。
要将millidegree转换为一个程度，只需将值除以1000。
"""

from sweeppy import Sweep, Sample
import csv, json
from time import time, sleep


def write_csv(scans):
    filename = 'one_sample4.csv'
    headers = ['TIMESTAMP', 'AZIMUTH', 'DISTANCE', 'SIGNAL_STRENGTH']
    with open(filename, 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        for scan in scans:
            for i, sample in enumerate(scan.samples):
                # sample: Sample
                if i == 0:
                    row = [int(time() * 1000), sample.angle / 1000, sample.distance, sample.signal_strength]
                else:
                    row = [-1, sample.angle / 1000, sample.distance, sample.signal_strength]
                f_csv.writerow(row)


def write_json(scans):
    filename = 'one_sample2.json'
    Sweeps = []
    for scan in scans:

        d = {'TimeStamp': int(time() * 1000)}
        SensorReading_Angles = []
        SensorReading_Radii = []
        SensorReading_SignalStrength = []
        for sample in scan.samples:
            SensorReading_Angles.append(sample.angle / 1000)
            SensorReading_Radii.append(sample.distance)
            SensorReading_SignalStrength.append(sample.signal_strength)
        d['SensorReading_Angles'] = SensorReading_Angles
        d['SensorReading_Radii'] = SensorReading_Radii
        d['SensorReading_SignalStrength'] = SensorReading_SignalStrength
        Sweeps.append(d)

    rs = {
        'bSensorIsMobile': False,
        'bLogTimeStampPerSweep': True,
        'Sweeps': Sweeps,
    }

    with open(filename, 'w') as fp:
        json.dump(rs, fp)


from itertools import islice

if __name__ == '__main__':
    # with Sweep('/dev/ttyUSB0') as sweep:
    with Sweep('/dev/tty.usbserial-DM00KZW7') as sweep:
        print('start_scanning')
        sweep.start_scanning()
        print('sleep(5)')
        sleep(2)
        scan1 = sweep.get_scans()
        # scan = scan1.__next__()
        # for scan in islice(sweep.get_scans(), 3):
        #
        # write_csv(scan)
        # scans = list(islice(sweep.get_scans(), 10))
        scans = []
        for _ in range(21):
            scan = scan1.__next__()
            scans.append(scan)
        # write_csv(scans)
        write_json(scans)

        print('stop_scanning')
        sweep.stop_scanning()
        sweep.set_motor_speed(0)
