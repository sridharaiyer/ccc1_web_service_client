from xmlutils import XMLUtils

xml = XMLUtils('S02_WorkfilePayload_input.xml')

costs = []
for elem in xml.root.iterfind('.//{*}NetRepairCost'):
    costs.append(float(elem.text))

print(max(costs))
