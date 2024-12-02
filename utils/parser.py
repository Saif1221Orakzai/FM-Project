import xml.etree.ElementTree as ET
from lxml import etree

def validate_xml_schema(filepath):
    schema_file = 'schema.xsd'  # Path to your schema file
    try:
        schema = etree.XMLSchema(file=schema_file)
        parser = etree.XMLParser(schema=schema)
        with open(filepath, 'r') as file:
            etree.parse(file, parser)
        return True
    except etree.XMLSchemaParseError as e:
        print(f"Schema parsing error: {e}")
        return False
    except etree.XMLSyntaxError as e:
        print(f"XML syntax error: {e}")
        return False
    except Exception as e:
        print(f"General error: {e}")
        return False

def parse_feature_model(filepath):
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()

        if root.tag != 'featureModel':
            raise ValueError("Root element must be 'featureModel'")

        feature_model = {'features': [], 'constraints': []}

        for feature in root.findall('.//feature'):
            feature_name = feature.get('name')
            mandatory = feature.get('mandatory', 'false').lower() == 'true'
            feature_model['features'].append({
                'name': feature_name,
                'mandatory': mandatory,
                'groups': parse_groups(feature)
            })

        for constraint in root.findall('.//constraints/constraint'):
            statement = constraint.find('englishStatement')
            if statement is not None:
                feature_model['constraints'].append(statement.text)

        return feature_model

    except ET.ParseError as e:
        raise ValueError(f"XML parsing error: {e}")

def parse_groups(feature_element):
    groups = []
    for group in feature_element.findall('.//group'):
        group_type = group.get('type')
        group_features = [f.text for f in group.findall('feature') if f.text]
        groups.append({'type': group_type, 'features': group_features})
    return groups
