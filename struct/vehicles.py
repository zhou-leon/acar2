import xml.etree.ElementTree as ET
import datafile
import vehicleConst as const
import events
import eventConst


class Vehicles:
    def __init__(self):
        self.tree = ET.parse(datafile.VEHICLES)
        self.root = self.tree.getroot()
        self._enum_cars()
        self.record_count = 0
        for car in self.show():
            self.record_count += len(self.get_records(car))

    def _enum_cars(self):
        pass

    def get_rec_count(self):
        return self.record_count

    def inc_rec_count(self):
        self.record_count += 1

    def find(self, name):
        for car in self.root:
            if name == car.find("name").text:
                return car
        return None

    def show(self):
        cars = []
        for car in self.root:
            cars.append(car.find("name").text)
        return cars

    def save(self):
        ET.indent(self.tree, space="    ")
        self.tree.write(datafile.VEHICLES)

    def addcar(self, name):
        v = ET.Element("vehicle")
        v.set("id", str(len(self.root) + 1))
        vname = ET.SubElement(v, "name")
        vname.text = name
        for ele in const.vehicle_attrib:
            sub = ET.SubElement(v, ele)
        self.root.append(v)

    def get_records(self, name):
        car = self.find(name)
        if name == None:
            return None
        return car.find("event-records")

    def get_info(self, name):
        car = self.find(name)
        if name == None:
            return None

        attribs = [
            "year",
            "make",
            "model",
            "engine",
            "transmission",
            "license-plate",
            "vin",
            "insurance-policy",
            "color",
        ]
        result = {}
        for attr in attribs:
            result[attr] = car.find(attr).text
        return result

    def find_by_id(self, vid):
        for car in self.root:
            if str(car.get('id')) == str(vid):
                return car
        return None

def test0():
    cars = Vehicles()
    e = events.Events()
    count = 0
    for car in cars.show():
        # e.gen_rpt(cars.get_records("Lexus RX"))
        count += len(cars.get_records(car))
    print(count)
    print(cars.get_rec_count())


def main():
    cars = Vehicles()
    for car in cars.show():
        print(cars.get_info(car))


if __name__ == "__main__":
    main()
