import random
import logging

from base import AbstractSensor


logger = logging.getLogger(__name__)


class DistanceSensor(AbstractSensor):
    """Sensor device for measuring distance."""

    def _send_message(self):
        distance = random.random() * 100
        logger.info({"distance": distance})
