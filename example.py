"""Simple DistanceSensor class usage example."""
import logging
import time
from sensors import DistanceSensor


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sensor = DistanceSensor()

    sensor.control(power=True, rateHz=10)
    time.sleep(2)
    sensor.control(power=False)

    # sleep a bit and resume sending data
    time.sleep(1)

    sensor.control(power=True, rateHz=1)
    time.sleep(2)
    sensor.control(power=False)
