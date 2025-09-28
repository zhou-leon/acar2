import vehicles
import events
import pprint


def gen_report(car):
    v = vehicles.Vehicles()
    e = events.Events()
    output = e.gen_rpt_txt(v.get_records(car))
    return output


def get_info(car):
    v = vehicles.Vehicles()
    info = pprint.pformat(v.get_info(car), indent=4)
    return info
