from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os
from lxml import etree
import xml.etree.ElementTree as ET
import pandas as pd
from io import BytesIO

app = Flask(__name__)
load_dotenv('data.env')
openai_key = os.getenv('api_key')
openai.api_key = openai_key

@app.route('/xml_schema_validation', methods=['POST'])
def validate_xml_schema():
    # actual_xml
    actual_xml_root =  etree.fromstring(request.form.get('xml_data'))
    actual_xml = etree.tostring(actual_xml_root, encoding='utf-8', method='xml')
    # schema_root = etree.XML(xml_schema)
    schema_xml_root =  etree.fromstring(request.form.get('schema'))
    schema = etree.XMLSchema(schema_xml_root)
    xml_doc = etree.XML(actual_xml)
    if schema.validate(xml_doc):
        return jsonify("message", "XML is valid against the schema."), 200
    else:
        return jsonify("error", str(schema.error_log)), 400


@app.route('/xml_schema_validation_by_type', methods=['POST'])
def validate_xml_schema_by_type():
    # Get the uploaded file and report type
    data = request.files.get("data", None)
    report_type = request.form.get('report_type')
    xml_data = request.form.get('xml_data')

    # Validate required inputs
    if not data or not report_type or not xml_data:
        return jsonify({"message": "data file, report_type, and xml_data are required"}), 400

    # Parse the actual XML
    try:
        actual_xml_root = etree.fromstring(xml_data.encode('utf-16'))
        actual_xml = etree.tostring(actual_xml_root, encoding='utf-16', method='xml')
    except etree.XMLSyntaxError as e:
        return jsonify({"error": "Invalid XML format", "details": str(e)}), 400

    # Read the Excel file into a DataFrame
    try:
        excel_data = pd.read_excel(BytesIO(data.read()))
    except Exception as e:
        return jsonify({"error": "Invalid Excel file", "details": str(e)}), 400

    # Convert Excel data to a list of dictionaries
    processed_data = excel_data.to_dict(orient='records')

    # Find the schema for the given report type
    for item in processed_data:
        if item.get('type') == report_type:
            try:
                schema_xml_root = etree.fromstring(item['schema'].encode('utf-16'))
                schema = etree.XMLSchema(schema_xml_root)
            except (KeyError, etree.XMLSyntaxError) as e:
                return jsonify({"error": "Invalid schema", "details": str(e)}), 400

            # Validate the actual XML against the schema
            try:
                xml_doc = etree.XML(actual_xml)
                if schema.validate(xml_doc):
                    return jsonify({"message": "XML is valid against the schema."}), 200
                else:
                    return jsonify({"error": "XML validation failed", "details": str(schema.error_log)}), 400
            except etree.XMLSyntaxError as e:
                return jsonify({"error": "Error during validation", "details": str(e)}), 400

    # If no matching report type is found
    return jsonify({"error": "No matching schema found for the given report type."}), 400


@app.route('/validate_xml_schema', methods=['POST'])
def validate_xml():
    # Get the uploaded file and report type
    xml_data = request.form.get('xml_data')
    # report_type = request.form.get('report_type')
    if not xml_data:
        return jsonify({"message": "xml_data is required"}), 400
    root = ET.fromstring(xml_data)
    xsd_name = root.tag
    # actual_xml
    try:
        actual_xml_root = etree.fromstring(xml_data.encode('utf-16'))
        actual_xml = etree.tostring(actual_xml_root, encoding='utf-16', method='xml')
    except etree.XMLSyntaxError as e:
        return jsonify({"error": "Invalid XML format", "details": str(e)}), 400
    # schema_root = etree.XML(xml_schema)
    try:
        with open(f"{xsd_name}.xsd", "rb") as f:
            file_content = f.read()
    except:
        return jsonify({"error": "XSD file not found", "details": str(e)}), 400

    try:
        schema_xml_root =  etree.fromstring(file_content)
        schema = etree.XMLSchema(schema_xml_root)
    except (KeyError, etree.XMLSyntaxError) as e:
                return jsonify({"error": "Invalid schema", "details": str(e)}), 400
    
    xml_doc = etree.XML(actual_xml)
    if schema.validate(xml_doc):
        return jsonify("message", "XML is valid against the schema."), 200
    else:
        return jsonify("error", str(schema.error_log)), 400
