import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from dragon_loop.models import Bus, Route, Location, Stop, Transponder


class BusType(DjangoObjectType):
    class Meta:
        model = Bus


class CreateBus(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    bus = graphene.Field(BusType)

    def mutate(parent, info, name):
        bus = Bus(name=name)
        ok = True
        bus.save()
        return CreateBus(bus=bus, ok=ok)


class BusMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String()

    bus = graphene.Field(BusType)
    ok = graphene.Boolean()

    def mutate(self, info, id, name):
        bus = Bus.objects.get(id=id)
        bus.name = name
        ok = True
        try:
            bus.save()
        except Exception:
            ok = False
        return BusMutation(bus=bus, ok=ok)


class RouteType(DjangoObjectType):
    class Meta:
        model = Route


class LocationType(DjangoObjectType):
    class Meta:
        model = Location


class StopType(DjangoObjectType):
    class Meta:
        model = Stop


class TransponderType(DjangoObjectType):
    class Meta:
        model = Transponder


class Query(ObjectType):
    bus = graphene.Field(
        BusType,
        description="A Bus",
        id=graphene.ID(description="Database ID", required=False),
        name=graphene.String(description="Bus Name", required=False),
    )
    busses = graphene.List(BusType, description="A List of Busses")

    route = graphene.Field(RouteType)
    routes = graphene.List(RouteType)

    location = graphene.Field(LocationType)
    locations = graphene.List(LocationType)

    stop = graphene.Field(StopType)
    stops = graphene.List(StopType)

    transponder = graphene.Field(TransponderType)
    transponders = graphene.List(TransponderType)

    def resolve_bus(self, info, **kwargs):
        filters = {k: i for (k, i) in kwargs.items() if i}
        return Bus.objects.filter(**filters).first()

    def resolve_busses(self, info, **kwargs):
        return Bus.objects.all()

    def resolve_routes(self, info, **kwargs):
        return Route.objects.all()

    def resolve_locations(self, info, **kwargs):
        return Location.objects.all()

    def resolve_stops(self, info, **kwargs):
        return Stop.objects.all()

    def resolve_transponders(self, info, **kwargs):
        return Transponder.objects.all()


class Mutation(ObjectType):
    update_bus = BusMutation.Field()
    create_bus = CreateBus.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
