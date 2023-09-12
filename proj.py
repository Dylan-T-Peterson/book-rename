import urllib.request as request
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
) -> request.Request:
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

    user_search = input("Input search terms: ")

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
    for key, val in keywords.items():
        getrequest = getrequest + f"+{key}{val}"
    getrequest = getrequest + f"&key={api_key}"
    req = request.Request(getrequest)
    response = request.urlopen(req).read()

    return response


def google_api_parser(api_response: str):
    pass


def title_epub(file: str):
    # Filters out any file w/o valid title metadata
    NONOCHARS = r"""#%*/+={}<>\$@"'`|!?"""
    CHARPAIRS = {
        "&": "and",
        "-": " ",
        "_": " ",
        ": ": "_",
        " ": "-",
    }

    try:
        book = epub.read_epub(file)
    except Exception as e:
        print(f"\n\n{file}\n{e} -- err\n\n")
        return

    # Pulls and processes Title Metadata for second verification
    identifier = book.get_metadata("DC", "identifier")
    if "ISBN" in identifier[0][1].values():
        isbn = identifier[0][0]
        isbn = isbn.strip(
            f"""{
                    string.ascii_letters,
                    string.punctuation,
                    string.whitespace
                    }""",
        )
        if len(isbn.replace("-", "")) not in (10, 13):
            print(f"\n\n{file}\nBook does not have a valid ISBN -- err\n\n")
            return

        print(file)
        print(isbn, "\n")
        title = ""

    else:
        title = book.get_metadata("DC", "title")[0][0]

    for var in (" /", "/"):
        title = title.split(var)[0]

    for char in NONOCHARS:
        title = title.replace(char, "")

    for old, new in CHARPAIRS.items():
        title = title.replace(old, new)
    title = title.lower()

    if title != "":
        print(f"\n{title} - {file}\n")


def main():
    path = "books/"
    api_key = open("apikey.txt", "r").read()

    for file in iglob(f"{path}*.epub"):
        title_epub(file)


if __name__ == "__main__":
    main()
