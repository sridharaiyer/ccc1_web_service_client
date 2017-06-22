from xmlutils import XMLUtils

files_dict = {
    "Workfile": [
        "raw/091_c.txt",
        "raw/158_c.txt",
        "raw/211_c.txt"
    ],
    "PrintImage": [
        "raw/092_c.txt",
        "raw/094_c.txt",
        "raw/095_c.txt",
        "raw/159_c.txt",
        "raw/161_c.txt",
        "raw/162_c.txt",
        "raw/212_c.txt",
        "raw/214_c.txt",
        "raw/215_c.txt"
    ],
    "DigitalImage": [
        "raw/093_c.txt",
        "raw/160_c.txt",
        "raw/213_c.txt"
    ],
    "StatusChange": [
        "raw/117_c.txt",
        "raw/172_c.txt",
        "raw/225_c.txt"
    ]
}


class EstmateDict(object):
    """docstring for EstmateDict"""

    def __init__(self, files_dict):
        self.files_dict = files_dict
        self.est_dict = {'E01': None}  # An estimate will have minimum E01

    def get_estimate_dict(self):
        highest_estimate = len(self.files_dict['Workfile'])
        if highest_estimate > 1:
            for i in range(highest_estimate - 1):
                e = ''
                if i < 9:
                    e = 'S0' + str(i + 1)
                else:
                    e = 'S' + str(i + 1)
                self.est_dict[e] = None
        print(self.est_dict)


if __name__ == '__main__':
    est_dict = EstmateDict(files_dict)
    est_dict.get_estimate_dict()
