import xml.etree.ElementTree as ET

def parse_feature_model(filepath):
    try:
        # Parse the XML content
        tree = ET.parse(filepath)
        root = tree.getroot()

        # Check if the root element exists and is 'featureModel'
        if root is None or root.tag != 'featureModel':
            raise ValueError("Root element 'featureModel' not found in XML")

        # Create a feature model object
        feature_model = {
            'features': [],
            'constraints': []
        }

        # Parse features
        for feature in root.findall('.//feature'):
            feature_name = feature.get('name')
            mandatory = feature.get('mandatory', 'false').lower() == 'true'
            feature_model['features'].append({
                'name': feature_name,
                'mandatory': mandatory,
                'groups': parse_groups(feature)
            })

        # Parse constraints if they exist
        for constraint in root.findall('.//constraints/constraint'):
            english_statement = constraint.find('englishStatement')
            if english_statement is not None:
                feature_model['constraints'].append(english_statement.text)

        return feature_model

    except ET.ParseError as e:
        raise ValueError(f"Error parsing XML: {e}")
    except Exception as e:
        raise ValueError(f"An error occurred: {e}")

def parse_groups(feature_element):
    groups = []
    for group in feature_element.findall('.//group'):
        group_type = group.get('type')
        group_features = [f.text for f in group.findall('feature')]
        groups.append({
            'type': group_type,
            'features': group_features
        })
    return groups