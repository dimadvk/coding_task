import abc

from sensors.exceptions import SensorError
from utils import validate_sensor_power
import logging
import threading


logger = logging.getLogger(__name__)


class AbstractSensor(object):
    __metaclass__ = abc.ABCMeta

    ALLOWED_RATE_HZ = (1, 10, 100)
    STOP_TIMEOUT = 1

    def __init__(self):
        self._power = False
        self._rate_hz = self.ALLOWED_RATE_HZ[0]

        self._should_stop = threading.Event()
        self._thread = None

    def control(self, power, rateHz=ALLOWED_RATE_HZ[0]):
        """Switch on/off the sensor and set data transmission frequency.

        Args:
            power (bool): sensor power state
            rateHz (int): data transmission frequency, Hz

        Returns:
            dict: {"acknowledge": True | False}
        """
        validate_sensor_power(power)

        if power == self._power:
            logger.debug("Sensor power state is the same as given.")
            return {"acknowledge": False}

        if rateHz not in self.ALLOWED_RATE_HZ:
            logger.debug("This rateHz value is not allowed!")
            return {"acknowledge": False}

        self._power = power
        self._rate_hz = rateHz

        if self._power:
            self._start()
        else:
            self._stop()

        return {"acknowledge": True}

    def _start(self):
        self._should_stop.clear()
        self._thread = threading.Thread(target=self._transmit_data)
        self._thread.daemon = True
        self._thread.start()
        logger.info("Data message starts being sent")

    def _stop(self):
        self._should_stop.set()
        self._thread.join(self.STOP_TIMEOUT)

        if self._thread.is_alive():
            msg = "Data transmission did not stop in a reasonable amount of time"
            logger.error(msg)
            raise SensorError(msg)

        self._thread = None
        logger.info("Data message stops being sent")

    def _transmit_data(self):
        while not self._should_stop.wait(1.0 / self._rate_hz):
            data = self._prepare_data()
            self._send_message(data)

    @abc.abstractmethod
    def _send_message(self, data):
        """Send measured data.

        Args:
            data (dict): measured data prepared for sending
        """

    @abc.abstractmethod
    def _prepare_data(self):
        """Prepare measured data.

        Returns:
            dict: measured data prepared for sending
        """
