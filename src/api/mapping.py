from api.schemas import ObservableSchema


class Sighting:
    def __init__(self, observable: ObservableSchema):
        pass

    def extract(self, alert: dict) -> dict:
        pass
