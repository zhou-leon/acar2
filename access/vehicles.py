import xml.etree.ElementTree as ET
import datafile
import vehicleConst as const
import events


class Vehicles:
    def __init__(self):
        """Initialize Vehicles by loading XML data and counting records."""
        self.tree = ET.parse(datafile.VEHICLES)
        self.root = self.tree.getroot()
        self._enum_cars()
        self.record_count = 0
        for car in self.show():
            records = self.get_records(car)
            if records is not None:
                self.record_count += len(records)

    def _enum_cars(self):
        """Placeholder for car enumeration logic (currently unused)."""
        pass

    def get_rec_count(self):
        """Return the total number of event records across all vehicles."""
        return self.record_count

    def inc_rec_count(self):
        """Increment the record count by one."""
        self.record_count += 1

    def find(self, name):
        """Find and return the car XML element by name."""
        for car in self.root:
            if name == car.find("name").text:
                return car
        return None

    def show(self):
        """Return a list of all car names in the database."""
        cars = []
        for car in self.root:
            cars.append(car.find("name").text)
        return cars

    def save(self):
        """Save the current state of the vehicles XML to disk."""
        ET.indent(self.tree, space="    ")
        self.tree.write(datafile.VEHICLES)

    def addcar(self, name, attrdic):
        """Add a new car to the database with the given attributes."""
        v = ET.Element("vehicle")
        v.set("id", str(len(self.root) + 1))
        vname = ET.SubElement(v, "name")
        vname.text = name
        for ele in const.vehicle_attrib:
            sub = ET.SubElement(v, ele)
            sub.text = attrdic.get(ele, "")
        self.root.append(v)

    def get_records(self, name):
        """Return the event records XML element for the given car name."""
        car = self.find(name)
        if name == None:
            return None
        return car.find("event-records")

    def get_info(self, name):
        """Return a dictionary of key attributes for the given car name."""
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
        """Find and return the car XML element by vehicle ID."""
        for car in self.root:
            if str(car.get('id')) == str(vid):
                return car
        return None

def test0():
    """Test function to count all event records for all cars."""
    cars = Vehicles()
    e = events.Events()
    count = 0
    for car in cars.show():
        # e.gen_rpt(cars.get_records("Lexus RX"))
        count += len(cars.get_records(car))
    print(count)
    print(cars.get_rec_count())


def main():
    """Main function to print info for all cars in the database."""
    cars = Vehicles()
    for car in cars.show():
        print(cars.get_info(car))


if __name__ == "__main__":
    main()
