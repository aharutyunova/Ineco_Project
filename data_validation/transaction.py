# import requests
# import asyncio
# import asyncpg
# import xml.etree.ElementTree as ET
# import xmltodict
# import json

# data = {"dsname": "_trreg_transactions", "datestart": "28/01/2025"}
# transaction_esb = "http://esb-test.ineco.com/api/Datasource?dsname=_trreg_transactions"
# headers = {"token": "cuduccdqt98w60qmkqj63m5jn45865i0", "callerid": "volo"}

# esb_request_result = requests.get(transaction_esb, data=data, headers=headers)
# esb_data = esb_request_result.json()['rows']
# # get first result in this example, need to get transaction by  any unique value - need to confirm
# compared_data = esb_data[0]

# async def get_xml(id):
#     conn = await asyncpg.create_pool(
#         user="ineco",
#         password="ineco@20@%",
#         database="ineco_transactions_dev",
#         host="10.11.51.174"
#     )
    
#     data = await conn.fetchrow(f'SELECT "Content" FROM public."DocumentTrackings" where "Id"={id}')
#     await conn.close()
#     if data is not None:
#         # Extract the XML content from the record
#         xml_content = data['Content']
#         xml_data = xmltodict.parse(xml_content)['report_banks_acc']
#         # Parse the XML content
#         print(xml_content)
#         return xml_data

# xml_dict = asyncio.run(get_xml(1916))

# keys_of_json = list(compared_data.keys())

# # get xml data
# xml_full_data = {}
# xml_dict_values = []
# xml_dict_values.append(xml_dict.get("report_name"))
# xml_dict_values.append(xml_dict.get("transaction_description"))
# xml_dict_values.append(xml_dict.get("transaction_type"))
# xml_dict_values.append(xml_dict.get("side_section"))

# for value in xml_dict_values:
#     if isinstance(value, list):
#         xml_full_data["side_section"] = value
#     elif value:
#          xml_full_data.update(value)

# print(xml_full_data)
# print("--------------------------------------------------------------------------------")
# print(compared_data)
import ftfy
import requests
import base64
import unicodedata
from unidecode import unidecode
import chardet
import charset_normalizer
from libasciitounicode.converter import Font, to_unicode

# The given incorrect text (misencoded)
# incorrect_text = b"äÈÚàôê 1 Èààô ¶ðàôä êäÀ"
# print(chardet.detect(incorrect_text))

# The correct Armenian text you want to compare with
a= {'@id': '1', 'side_type': '1', 'side_subtype': '2', 'company_name': 'ՄԱՈՒՆԹԱՅՆ ՊԼԱԶԱ ՍՊԸ', 'leg_org_form': '01', 'other_leg_org_form': None, 'manager_name': 'Խաչիկ Ավդալյան', 'tax_id': '04433715', 'reg_number': None}

print(isinstance(a, dict))