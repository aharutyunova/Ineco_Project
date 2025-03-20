import requests

def get_account_data(report_type):
    body = {
        "filter": {
            "logic": "And",
            "filters": [
                {
                    "field": "datestart",
                    "value": "28/01/2025"
                }
            ]
        }}
    account_open_esb = f"http://esb-test.ineco.com/api/Datasource?dsname={report_type}"
    headers = {"token": "cuduccdqt98w60qmkqj63m5jn45865i0", "callerid": "volo"}

    esb_request_result = requests.post(account_open_esb, json=body, headers=headers)
    esb_data = esb_request_result.json()['rows']
    # get first result in this example, need to get transaction by  any unique value - need to confirm
    compared_data = esb_data
    return compared_data


