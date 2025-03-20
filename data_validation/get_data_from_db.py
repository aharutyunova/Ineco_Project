import asyncio
import asyncpg
import xmltodict
import json

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
        xml_data = xmltodict.parse(xml_content)['report_banks_acc']
        # Parse the XML content
        # print(xml_content)
        return xml_data

