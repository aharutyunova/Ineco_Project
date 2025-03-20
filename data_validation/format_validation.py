import get_data_from_esb
import get_data_from_db
import asyncio
import asyncio
import asyncpg
import xmltodict
import json
import requests
import logging

logging.basicConfig(
     filename='validation.log',
     level=logging.INFO, 
     format= '[%(asctime)s] { %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )

async def get_xml(account):
    conn = await asyncpg.create_pool(
        user="ineco",
        password="ineco@20@%",
        database="ineco_accounts_dev",
        host="10.11.51.174"
    )
    
    data = await conn.fetchrow(f"""SELECT "Content" FROM public."DocumentTrackings" where "EntityIdentifier"= '{account}'""")
    await conn.close()
    if data is not None:
        # Extract the XML content from the record
        xml_content = data['Content']
        xml_data = xmltodict.parse(xml_content)
        # Parse the XML content
        # print(xml_content)
        return xml_content

def remove_xml_declaration_simple(xml_string):
    # Check if XML declaration exists and remove it
    if xml_string.startswith('<?xml'):
        return xml_string.split('?>', 1)[-1].strip()
    return xml_string

all_json_data = get_data_from_esb.get_account_data('_acreg_account_close')

for json_data in all_json_data:
    account = json_data['account_id']
    print(account)
    xml_data = asyncio.run(get_xml(account))
    xml_data = remove_xml_declaration_simple(xml_data)
    
    data = {
        'xml_data': xml_data}
    
    response = requests.post('https://xml-validation.onrender.com/validate_xml_schema', data=data)
    response_data = response.json()
    if len(response_data) > 0:
        if response_data[0] == "error":
            logging.error(f"for account {account}, response is {response_data}")
        else:
            logging.info(f"for account {account}, response is {response_data}")
