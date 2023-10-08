import urllib
import re
import urllib.request as request
import json
import string
from glob import iglob

from ebooklib import epub


# def google_api_req_generator(
def test(
    api_key: str,
    intitle: str = "",
    inauthor: str = "",
    inpublisher: str = "",
    subject: str = "",
    isbn: str = "",
    lccn: str = "",
    oclc: str = "",
    userin: str = "",
) -> dict[str, str]:
    uri = "https://www.googleapis.com/books/v1/volumes?q="
    api_key = api_key
    keywords = {
        "intitle:": f"{intitle}",
        "inauthor:": f"{inauthor}",
        "inpublisher:": f"{inpublisher}",
        "subject:": f"{subject}",
        "isbn:": f"{isbn}",  # International Standard Book Number
        "lccn:": f"{lccn}",  # Library of Congress Control Number
        "oclc:": f"{oclc}",  # Online Computer Library Center Number
    }

    user_search = userin

    # Filters out empty parameters from keywords var
    nullkw = []
    for key in keywords:
        if keywords[key] == "":
            nullkw.append(key)
    for key in nullkw:
        del keywords[key]
    del nullkw

    # Creates request URI and sends it to Google Books API
    getrequest = uri + user_search
    if keywords != {}:
        for key, val in keywords.items():
            getrequest = getrequest + f"+{key}{val}"
    else:
        return {}
    getrequest = getrequest + f"&key={api_key}"
    getrequest = re.sub(r"[^\x00-\x7F]+", "", getrequest)
    req = request.Request(getrequest)
    try:
        response = request.urlopen(req).read().decode()
    except request.HTTPError:
        print(f"isbn='{isbn}' k,v={keywords} {getrequest} // bad req -- err")
        return {}
    response = json.loads(response)
    return response


def title_epub(file: str, apikey: str = ""):
    # Filters out any file w/o valid title metadata
    NONOCHARS = r"""#%*/+={}<>\$@"'`|!?"""
    CHARPAIRS = {
        "&": "and",
        "-": " ",
        "_": " ",
        ": ": "_",
        " ": "-",
    }
    title = ""

    try:
        book = epub.read_epub(file)
    except Exception as e:
        print(f"\n\n{file} // {e} -- err\n\n")
        return

    # Pulls and processes Title Metadata for second verification
    identifier = book.get_metadata("DC", "identifier")
    if (apikey != "") and ("ISBN" in identifier[0][1].values()):
        # while title == "":
        isbn = identifier[0][0]
        isbn = isbn.strip(
            f"""{
                    string.ascii_letters,
                    string.punctuation,
                    string.whitespace
                    }""",
        )
        isbn = isbn.replace("-", "")
        if len(isbn) not in (10, 13):
            title = book.get_metadata("DC", "title")[0][0]

        api_response = test(api_key=apikey, isbn=isbn)
        if ("totalItems" in api_response) and (int(api_response["totalItems"]) > 0):
            title = api_response["items"][0]["volumeInfo"]["title"]
        else:
            title = book.get_metadata("DC", "title")[0][0]

    else:
        title = book.get_metadata("DC", "title")[0][0]

    for var in (" /", "/" " :", ": "):
        title = title.split(var)[0]

    for char in NONOCHARS:
        title = title.replace(char, "")

    for old, new in CHARPAIRS.items():
        title = title.replace(old, new)
    title = title.lower()
    title = title + ".epub"

    if title == "":
        print(f"\n\n{file} {title} // no title -- err\n")
        return
    return title


def main():
    path = "books/"
    api_key = open("apikey.txt", "r").read()

    for file in iglob(f"{path}*.epub"):
        print(title_epub(file=file, apikey=api_key))


if __name__ == "__main__":
    # try:
    main()
    # except Exception as e:
    #     print(f"\n\n\n{e}\n\n\n")
