import re
from difflib import get_close_matches


def extractorganization(text, orgsfile="./optimaUtils.txt"):
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

    matches, cutoff = find_close_matches_with_threshold(clean_text,organizations)

    if len(matches) == 1:
        return matches[0]
    else:
        return matches


def find_close_matches_with_threshold(target, words, step=0.001, cutoff=0.1, n=1):
    matches = []
    while len(matches) < n and cutoff > 0:
        matches = get_close_matches(target, words, n=n, cutoff=cutoff)
        cutoff -= step
    return matches, cutoff + step


# todo find closest word for keyword then perform regex on that
def extractpaymentid(text):

    # patterns = ["Л/счет[\s\S]{0,3}?(\d[\d\s-]*\d|\d)",
    #     r"(?i)Лицевой[\s\S]*?счет[\s\S]{0,10}?(\d[\d\s-]*\d|\d)",
    # r"(?i)счет[\s\S]{0,10}?(\d[\d\s-]*\d|\d)",
    # r"(?i)Лицевой[\s\S]{0,10}?(\d[\d\s-]*\d|\d)"
    #             ]
    # total = []
    # for pattern in patterns:
    #     matches = re.findall(pattern, text)
    #     if clean_and_remove_duplicates(matches):
    #         total.extend(matches)
    #         break
    #
    # total = clean_and_remove_duplicates(total)
    #
    #
    # return total[0] if len(total) == 1 else total

    t = "Л/счет Лицевой счет"
    pattern = "[\s\S]{0,15}?(\d[\d\s-]*\d|\d)"

    matches, cut = extract_by_closest_match(text, t, pattern)

    return clean_and_remove_duplicates(matches)


def extractperiod(text):
    period = re.findall("(?i)Период([\s0-9.,-]+)+", text)

    periods = clean_and_remove_duplicates(period)
    return periods[0] if len(periods) == 1 else periods


def extractamount(text):
    patterns = [
        "(?i)Итого\sк\sоплате\s([0-9.,]+)+",
        "(?i)к\sоплате\s:?([0-9.,]+)+",
        "(?i)оплате\s([0-9.,]+)+",
        # "(?i)К\sоплате\sза\sэл\.зн.{0,10}(\d[\d,.]*\d|\d)",
        "(?i)оплате\sза\sэл\.зн,\s(\d[\d,.]*\d|\d)",
        "(?i)Итого\sк\sоплате[\s\S]{0,10}?(\d[\d,.]*\d|\d)",
        "(?i)к\sоплате[\s\S]{0,10}?(\d[\d,.]*\d|\d)",

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

    # t0 = "Итого к оплате"
    # t1 = "к оплате"
    # t2 = "оплате"
    # t3 = "оплате за sэл .зн"
    #
    # pattern = "[\s\S]{0,15}?(\d[\d\s-]*\d|\d)"
    #
    # return clean_and_remove_duplicates(extract_by_closest_match(text, t0, pattern))


def clean_and_remove_duplicates(matches):
    cleaned_matches = []

    for match in matches:
        # Remove whitespace and newline characters
        cleaned_match = match.replace(" ", "").replace("\n", "")

        # Add cleaned match to the list if it's not already there
        if cleaned_match not in cleaned_matches and len(cleaned_match) != 0:
            cleaned_matches.append(cleaned_match)

    return cleaned_matches


def extract_by_closest_match(text,target,regex):

    words = text.split()
    closest, cutoff = find_close_matches_with_threshold(target, words)
    final_pattern = closest[0].__str__() + regex
    matches = re.findall(final_pattern, text)
    return matches, cutoff


if __name__ == "__main__":
    mytext = """your ocr output"""
    # organizations_location = "optimaUtils.txt"
    t = "Л/счет Лицевой счет"
    pattern = "[\s\S]{0,15}?(\d[\d\s-]*\d|\d)"
    print(extractpaymentid(mytext))

    # print(extractorganization(text, organizations_location, 1))
