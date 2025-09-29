import xml.etree.ElementTree as ET
import datafile
import eventConst as const


class Events:
    def __init__(self):
        """Initialize Events by loading event subtype XML data."""
        self.st = ET.parse(datafile.EVENT_SUBTYPES)
        self.st_root = self.st.getroot()

    # pass a map[string]string of record fields
    # dic[subfields] is a list
    def gen_from_dic(self, dic):
        """Generate an XML event record from a dictionary of event fields."""
        r = ET.Element(const.event_record_str)
        lookup = self.get_subtypes()
        # everything except for subtype
        for f in dic:
            # deal with subtypes later
            if f == const.subtypes_str:
                continue
            sub = ET.SubElement(r, f)
            if not dic[f] == "":
                sub.text = dic[f]
        subtypes = ET.SubElement(r, const.subtypes_str)
        for s in dic[const.subtypes_str]:
            subt = ET.SubElement(subtypes, const.subtype_str)
            id = lookup[s][const.id_str]
            subt.set(const.id_str, id)
        return r

    # add a single event record of ET.Element type
    # modifies existing ID
    def add_rec(self, recs, r, count):
        """Add a single event record to the records XML, updating its ID."""
        r.set(const.id_str, str(count))
        recs.insert(0, r)

    # generate a template to be filled in later
    def gen_template(self, recs, count):
        """Generate a blank event record template with the given count as ID."""
        r = ET.Element(const.event_record_str)
        r.set(const.id_str, str(count))
        for f in const.event_record:
            sub = ET.SubElement(r, f)
        return r

    def gen_rpt(self, recs):
        """Print a formatted event report for the given records XML."""
        print(self.gen_rpt_txt(recs))

    def gen_rpt_txt(self, recs):
        """Return a formatted string report for the given records XML."""
        output = ""
        for rec in recs:
            for f in rec:
                if not (f.text == None or f.tag in const.ignore):
                    output += "{}: {}\n".format(f.tag, f.text)
            subs = rec.find(const.subtypes_str)
            for sub in subs:
                tag = sub.get(const.id_str)

                # match subtype ID against subtype definitions
                for st in self.st_root:
                    if tag == st.get(const.id_str):
                        type, _, name, _ = self.get_subtype_fields(st)
                        output += "* {}: {}.\n".format(type, name)
            output += "==================================\n"
            output += "\n"
        return output

    def get_subtype_fields(self, st):
        """Extract and return subtype fields from a subtype XML element."""
        type = st.get(const.subtype_type_str)
        id = st.get(const.id_str)
        name = st.find(const.subtype_name_str).text
        notes = st.find(const.subtype_notes_str).text
        return type, id, name, notes

    # get supported subtypes as a dictionary
    def get_subtypes(self):
        """Return a dictionary of supported subtypes from the XML data."""
        subtypes = {}
        for st in self.st_root:
            type, id, name, notes = self.get_subtype_fields(st)
            subtypes[name] = {
                const.id_str: id,
                const.subtype_type_str: type,
                const.subtype_notes_str: notes,
            }
        return subtypes


def main():
    """Main function to print all supported subtypes."""
    e = Events()
    st = e.get_subtypes()
    print(st)


if __name__ == "__main__":
    main()
