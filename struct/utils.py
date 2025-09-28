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

def add_record(car, event_dic):
    v = vehicles.Vehicles()
    e = events.Events()

    # get pointer to current car's service record
    service_rec = v.get_records(car)

    # build a dic of a new record.
    new_event = e.gen_from_dic(event_dic)
    e.add_rec(service_rec, new_event, v.get_rec_count() + 1)
    v.save()
    v.inc_rec_count()
