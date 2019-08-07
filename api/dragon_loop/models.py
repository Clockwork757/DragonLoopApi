from django.db import models
#from django.contrib.gis.db import models as geo_models
from datetime import datetime


class Route(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}'


class Stop(models.Model):
    #location = geo_models.PointField()
    lat = models.FloatField()
    lon = models.FloatField()
    address = models.CharField(max_length=100)
    next_stop = models.OneToOneField(
        "self",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="last_stop",
    )
    route = models.ForeignKey(Route,
                              on_delete=models.DO_NOTHING,
                              null=True,
                              related_name="stops")

    def __str__(self):
        return f'"{self.address}" on Route: {self.route}'


class Bus(models.Model):
    name = models.CharField(max_length=50, unique=True)
    route = models.ForeignKey(Route,
                              on_delete=models.DO_NOTHING,
                              null=True,
                              related_name="busses")

    class Meta:
        verbose_name_plural = 'busses'

    def __str__(self):
        return f'{self.name} on Route: {self.route.name}'


class Location(models.Model):
    """
    Stores a Bus' location at a point in time
    """
    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
        related_name="location_history",
    )
    time = models.DateTimeField(default=datetime.now)
    lat = models.FloatField()
    lon = models.FloatField()

    #location = geo_models.PointField()

    def __str__(self):
        return f'{self.bus.name} at {self.lat},{self.lon} at {self.time}'


class Transponder(models.Model):
    """
    Represents the gps transponder on a bus
    """
    device_id = models.CharField(max_length=100, unique=True)
    bus = models.ForeignKey(Bus,
                            on_delete=models.DO_NOTHING,
                            null=True,
                            related_name="transponders")

    def __str__(self):
        return f'{self.device_id} on {self.bus.name}'