import random
import logging

from base import AbstractSensor


logger = logging.getLogger(__name__)


class DistanceSensor(AbstractSensor):
    """Sensor device for measuring distance."""

    def _send_message(self, data):
        logger.info("send data: %s" % data)

    def _prepare_data(self):
        distance = random.random() * 100
        return {"distance": distance}
