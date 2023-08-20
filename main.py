import requests
import json
import constants
import pandas as pd

def ch_call(target_company_number, api_endpoint, api_function="", query="", retries=0):
    """
    Main function for calling companies house API
    api_endpoints are search, company etc
    api_functions are typically the tabs you click on on the companies house website - overview, filing-history etc...
    Need an API key from https://developer.company-information.service.gov.uk/
    """
    base_url = "https://api.companieshouse.gov.uk"
    api_url = f"{base_url}/{api_endpoint}/{target_company_number}/{api_function}/?{query}"
    get_result = requests.get(api_url, headers={"Authorization": constants.api_key})

    output = json.loads(get_result.content)

    # API responses can be temperamental - often resolved by trying again
    if "error" in output and output["error"] == "Internal server error":
        retries += 1
        print("ERROR (retry " + str(retries) + "): " + api_endpoint + target_company_number + api_function + query)

        if retries <= 3:
            output = ch_call(target_company_number, api_endpoint, api_function, query, retries)
        else:
            output = False

    return output


def get_company_name(company_number, company_function=""):
    primary_function = "company"
    info_output = ch_call(company_number, primary_function)
    company_name = info_output.get("company_name")

    return company_name


def get_company_filings(company_number, company_function=""):
    primary_function = "company"
    filings_output = ch_call(company_number, primary_function, company_function)

    return filings_output


def main():
    target_company = '09263424'
    print(f"{'-'*25} {get_company_name(target_company)} {'-'*25}")
    response = get_company_filings(target_company, 'filing-history')

    df = pd.DataFrame(response['items'])
    print(df)


if __name__ == '__main__':
    main()
