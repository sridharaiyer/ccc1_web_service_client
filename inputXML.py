from xmlbase import CreateXML
import uuid


class Workfile(CreateXML):
    """docstring for Workfile"""

    def __init__(self, input_filename):
        self._input_filename = input_filename
        self._uuid = str(uuid.uuid4())
        super(Workfile, self).__init__()

    @property
    def uuid(self):
        return self._uuid

    def modifyXML(self):
        # Modify body
        super(Workfile, self).modifyXML()
        # Modifying the Payload
        super(Workfile, self).modifyXML(self.payload_root)

        payload = self.root_to_string(self.payload_root)
        modified_gzipped_payload = self.gzip_encode(payload)

        self.replace_tag(tag='.//{*}Data', data=modified_gzipped_payload)

        # Change reference UUID
        super(Workfile, self).change_reference(ref=self.uuid)
