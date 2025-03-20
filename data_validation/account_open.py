import requests
import asyncio
import xml.etree.ElementTree as ET
import xml_expected_structure
import get_data_from_db
import get_data_from_esb
import logging

logging.basicConfig(
     filename='accounts.log',
     level=logging.INFO, 
     format= '[%(asctime)s] { %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )
# BEFORE EXECUTION CHANGE REPORT TYPE
all_json_data = get_data_from_esb.get_account_data('_acreg_account_status')


for json_data in all_json_data:
    account = json_data['account_id']
    print(f"Account is {account}")
    xml_data = asyncio.run(get_data_from_db.get_xml(account))
    transaction_keys = xml_expected_structure.account_tags['transaction']
    # modify xml and json dictionaries
    json_data['account_number'] = json_data.pop("account_id")
    json_data['notes'] = json_data.pop("action")

    # get sections from json
    json_main_side= json_data.get("side_section_id")
    json_rel_author_section = json_data.get("rel_auth_side_section_id")

    def compare_side_section_data(key, side_number=0):
        key_json = key
        if side_number in (4,5):
            key_json = 'rel_auth_'+ key
        json_data_side_section = json_data.get(key_json)
        side_section_data = xml_data['side_section']
        if isinstance(side_section_data, dict):
            my_section_data = xml_data['side_section'].get(key)
        else:
            for i in range(len(side_section_data)):
                if int(side_section_data[i]['@id']) == int(side_number):
                    my_section_data = xml_data['side_section'][i].get(key)
        if key == "reg_number":
            if my_section_data == json_data_side_section:
                logging.info(f"Key {key}: XML data {my_section_data} equal Json data {json_data_side_section}")
            else:
                logging.error(f"{account}: for key {key} XML data {my_section_data} NOT equal Json data {json_data_side_section}")
        elif key == "reference_id":
            if float(xml_data['side_section'][i]['auth_clients'][key]) == float(json_data_side_section):
                 logging.info(f" Key {key}:XML data {my_section_data} equal Json data {json_data_side_section}")
            else:
                logging.error(f"{account}: for key {key}  XML data {my_section_data} NOT equal Json data {json_data_side_section}")
        elif my_section_data and  my_section_data.isdigit():
            if float(my_section_data) == float(json_data_side_section):
                logging.info(f"Key {key}: XML data {my_section_data} equal Json data {json_data_side_section}")
            else:
                logging.error(f"{account}: for key {key}  XML data {my_section_data} NOT equal Json data {json_data_side_section}")
        else:
            if my_section_data and any(ord(c) > 127 for c in my_section_data):
                logging.info(f"{key} value was in armenia")
                pass
            else:
                if my_section_data == json_data_side_section:
                    logging.info(f" Key {key}: XML data {my_section_data} equal {json_data_side_section}")
                else:
                    logging.error(f"{account}: for key {key}  XML data {my_section_data} NOT equal Json data {json_data_side_section}")
                

    # check transaction section
    for key in transaction_keys:
        json_data_transaction = json_data.get(key)
        xml_data_transaction = xml_data['transaction'].get(key)
        if xml_data_transaction.isdigit():
            if float(xml_data_transaction) == float(json_data_transaction):
                logging.info(f" Key {key}: XML data {xml_data_transaction} equal {json_data_transaction}")
            else:
                logging.error(f"{account}: XML data {xml_data_transaction} equal Json data {json_data_transaction}")
        else:
            if xml_data_transaction == json_data_transaction:
                logging.info(f"Key {key}: XML data {xml_data} don't equal {json_data_transaction}")
            else:
                logging.error(f"{account}: XML data {xml_data_transaction} equal Json data {json_data_transaction}")
    # check main side section
    if json_main_side == 0.0:
        for key in xml_expected_structure.account_tags['side_section_id_0']:
            compare_side_section_data(key, side_number=0)
    elif json_main_side == 1.0:
        for key in xml_expected_structure.account_tags['side_section_id_1']:
            compare_side_section_data(key, side_number=1)
    elif json_main_side == 2.0:
        for key in xml_expected_structure.account_tags['side_section_id_2']:
            compare_side_section_data(key,side_number=2)
    elif json_main_side == 3.0:
        for key in xml_expected_structure.account_tags['side_section_id_3']:
            compare_side_section_data(key, side_number=3)
    # check authorized side section
    if json_rel_author_section == 4.0:
        for key in xml_expected_structure.account_tags['side_section_id_4']:
            compare_side_section_data(key, side_number=4)
    if json_rel_author_section == 5.0:
        for key in xml_expected_structure.account_tags['side_section_id_4']:
            compare_side_section_data(key, side_number=5)  