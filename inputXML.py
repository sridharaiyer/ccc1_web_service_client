from xmlbase import CreateXML
import uuid


class PutPendingXML(CreateXML):
    """docstring for PutPendingXML"""

    def __init__(self):
        super(PutPendingXML, self).__init__()

    def modifyXML(self):
        # Modify body
        super(PutPendingXML, self).modifyXML()
        # Modifying the Payload
        super(PutPendingXML, self).modifyXML(self.payload_root)

        payload = self.root_to_string(self.payload_root)
        modified_gzipped_payload = self.gzip_encode(payload)

        self.replace_tag(tag='.//{*}Data', value=modified_gzipped_payload)

        # Change reference UUID
        super(PutPendingXML, self).change_reference(ref=self.uuid)


class Workfile(PutPendingXML):
    """docstring for Workfile"""

    def __init__(self):
        super(Workfile, self).__init__()

    def modifyXML(self):
        super(Workfile, self).modifyXML()
