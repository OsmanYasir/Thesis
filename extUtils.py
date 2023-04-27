import re
from difflib import get_close_matches


def extractorganization(text, orgsfile="./optimaUtils.txt", n=5, cutoff=0.1, step=0.001):
    """
    Finds the closest matches in a list of organizations to a given text.

    Args:
    text (str): The text to match against the list of organizations.
    orgsfile (str): The filename of the file containing the list of organizations.
    n (int): The maximum number of matches to return.
    cutoff (float): The starting cutoff value for matching.
    step (float): The step size by which to decrease the cutoff value.

    Returns:
    A list of the closest matches in the list of organizations to the given text.
    """

    organizations = []
    with open(orgsfile, 'r', encoding='utf-8') as f:
        for line in f:
            organizations.append(line.strip())

    # Clean the text by removing newline characters and multiple spaces
    clean_text = re.sub(r'\n|\d+|\s{2,}', ' ', text).strip()

    matches = []

    while len(matches) < n and cutoff > 0:
        matches = get_close_matches(clean_text, organizations, n=n, cutoff=cutoff)
        cutoff -= step

    if len(matches) == 1:
        return matches[0]
    else:
        return matches


# todo find closest word for keyword then perform regex on that
def extractpaymentid(text):
    # todo remove unneccessary items from list

    id = re.findall("(?i)счет([\s0-9]+)+", text)
    if len(id) == 0:
        id = re.findall("(?i)чет([\s0-9]+)+", text)

    ids = clean_and_remove_duplicates(id)
    return ids[0] if len(ids) == 1 else ids


def extractperiod(text):
    period = re.findall("(?i)Период([\s0-9.,-]+)+", text)

    periods = clean_and_remove_duplicates(period)
    return periods[0] if len(periods) == 1 else periods

def extractamount(text):
    patterns = [
        "(?i)Итого\sк\sоплате\s([0-9.,]+)+",
        "(?i)к\sоплате\s([0-9.,]+)+",
        "(?i)оплате\s([0-9.,]+)+",
        # "(?i)К\sоплате\sза\sэл\.зн.{0,10}(\d[\d,.]*\d|\d)",
        "(?i)К\sоплате\sза\sэл\.зн,\s(\d[\d,.]*\d|\d)",
        "(?i)Итого\sк\sоплате.{0,10}(\d[\d,.]*\d|\d)",
        "(?i)к\sоплате.{0,10}(\d[\d,.]*\d|\d)",

        "(?i)оплате[^0-9]+([0-9.,]+)+"
    ]

    total = []

    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            total.extend(matches)
            break

    total = clean_and_remove_duplicates(total)
    return total[0] if len(total) == 1 else total


def clean_and_remove_duplicates(matches):
    cleaned_matches = []

    for match in matches:
        # Remove whitespace and newline characters
        cleaned_match = match.replace(" ", "").replace("\n", "")


        # Add cleaned match to the list if it's not already there
        if cleaned_match not in cleaned_matches and len(cleaned_match) != 0:
            cleaned_matches.append(cleaned_match)



    return cleaned_matches
if __name__ == "__main__":
    text = "your text"
    organizations_location = "optimaUtils.txt"
    print(extractorganization(text , organizations_location, 1))
