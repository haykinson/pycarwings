from xml.dom import minidom

def dict_to_xml(data, root_name, namespaces=None):
    doc = minidom.Document()
    root = doc.createElement(root_name)

    if namespaces:
        for ns_name, ns_uri in namespaces.iteritems():
            root.setAttribute('xmlns:%s' % ns_name, ns_uri)

    doc.appendChild(root)

    xml_add_dict(data, root, doc)

    return doc

def xml_add_dict(data, root, doc):
    for name, value in data.iteritems():
        if isinstance(value, list):
            xml_add_list(value, name, root, doc)
        else:
            xml_add_item(value, name, root, doc)

def xml_add_list(data, name, root, doc):
    for item in data:
        xml_add_item(item, name, root, doc)

def xml_add_item(data, name, root, doc):
    if isinstance(data, dict):
        node = doc.createElement(name)
        root.appendChild(node)
        xml_add_dict(data, node, doc)
    else:
        if name.startswith('@'):
            root.setAttribute(name[1:], data)
        else:
            node = doc.createElement(name)
            text = doc.createTextNode(str(data))
            node.appendChild(text)
            root.appendChild(node)


if __name__ == "__main__":
    d = { "child" : { "secondchild": 123 , "@attr": "attrvalue", "arrayname": [ {"alpha":"beta", "@alphabazattr":"alphavalue"}, {"gamma":"delta"} ], "anotherarray":[1,2,3]}}
    x = dict_to_xml(d, 'ns:root', {'ns':'uri:some:place'})
    print x.toprettyxml()
