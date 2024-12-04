from pydantic import BaseModel
import json


# {"origin": "Alice", "latitude": "44.833328", "longitude": "-0.56667", "altitude": 5000}
class LiveRecord(BaseModel):
    origin: str
    latitude: float
    longitude: float
    altitude: float
    orientation: int
    speed: float
    type: str

    def fromJson(json_playload):
        try:
            d = json.loads(json_playload)

            print(d)
            if (
                d["origin"] != None
                and d["latitude"] != None
                and d["longitude"] != None
                and d["altitude"] != None
                and d["orientation"] != None
                and d["speed"] != None
                and d["type"] != None
            ):
                return LiveRecord(
                    origin=d["origin"],
                    latitude=d["latitude"],
                    longitude=d["longitude"],
                    altitude=d["altitude"],
                    orientation=d["orientation"],
                    speed=d["speed"],
                    type=d["type"],
                )
            else:
                return None
        except Exception as e:
            print("error: json deserialize " + str(e))
            return None

    def toJson(self):
        try:
            return json.dumps(
                {
                    "origin": self.origin,
                    "latitude": self.latitude,
                    "longitude": self.longitude,
                    "altitude": self.altitude,
                    "orientation": self.orientation,
                    "speed": self.speed,
                    "type": self.type,
                }
            )
        except Exception as e:
            print("error in LiveRecord to json : " + str(e))
            return None
