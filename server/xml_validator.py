# Validação do esquema XML (XSD)

import xmlschema
from xmlschema.validators.exceptions import XMLSchemaValidationError


def validate_xml(file_path, xsd_path):
    try:
        schema = xmlschema.XMLSchema(xsd_path)
        schema.validate(file_path)
        print("XML validation successful.")
        return True, "XML is valid according to the schema."
    except XMLSchemaValidationError as e:
        print(f"XML validation error: {str(e)}")
        return False, f"Validation error: {str(e)}"
