from django.contrib import admin
from dragon_loop.models import Bus, Route, Stop, Location, Transponder


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    pass


@admin.register(Stop)
class StopAdmin(admin.ModelAdmin):
    pass


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Transponder)
class TransponderAdmin(admin.ModelAdmin):
    pass
