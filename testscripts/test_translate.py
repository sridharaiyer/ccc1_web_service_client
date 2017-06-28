data = {
    "E01": {
        "AdvisorService": [
            "raw/18_c.txt",
            "raw/33_c.txt"
        ],
        "Workfile": "raw/39_c.txt",
        "DigitalImage": ["raw/41_c.txt"],
        "Event": [
            "raw/44_c.txt",
            "raw/59_c.txt",
            "raw/60_c.txt",
            "raw/63_c.txt",
            "raw/64_c.txt",
            "raw/65_c.txt",
            "raw/66_c.txt",
            "raw/67_c.txt",
            "raw/68_c.txt",
            "raw/69_c.txt"
        ],
        "StatusChange": "raw/73_c.txt",
        "EstimatePrintImage": "raw/40_c.txt",
        "UnrelatedPriorDamage": "raw/42_c.txt",
        "RelatedPriorDamageReport": "raw/43_c.txt"
    },
    "S01": {
        "AnotherService": [
            "raw/18_c.txt",
            "raw/33_c.txt"
        ],
        "MyOwnClass": [
            "raw/44_c.txt",
            "raw/59_c.txt",
            "raw/60_c.txt",
            "raw/63_c.txt",
            "raw/64_c.txt",
            "raw/65_c.txt",
            "raw/66_c.txt",
            "raw/67_c.txt",
            "raw/68_c.txt",
            "raw/69_c.txt"
        ],
    }
}

objects = []
for estimate_type, v in data.items():
    for class_name, file_locations in v.items():
        if isinstance(file_locations, str):
            file_locations = [file_locations]
        for file_loc in file_locations:
            custom_class = type(class_name, (object,), {'file_loc': file_loc, 'estimate_type': estimate_type})
            obj_instance = custom_class()
            objects.append(obj_instance)

for obj in objects:
    print('object_class : {}, file_loc: {}, estimate_type: {}'.format(obj.__class__.__name__, obj.file_loc, obj.estimate_type))
