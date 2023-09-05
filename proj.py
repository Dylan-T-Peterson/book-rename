import urllib.request as request
import string
from glob import iglob

from ebooklib import epub


# def google_api_vol_req_generator(
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

    nullkw = []
    for key in keywords:
        if keywords[key] == "":
            nullkw.append(key)
    for key in nullkw:
        del keywords[key]
    del nullkw

    getrequest = uri + user_search
    for key, val in keywords.items():
        getrequest = getrequest + f"+{key}{val}"
    getrequest = getrequest + f"&key={api_key}"
    req = request.Request(getrequest)
    response = request.urlopen(req).read()

    return response


def google_api_parser(api_req: str):
    pass


def title_epub(file: str):
    try:
        book = epub.read_epub(file)
    except Exception as e:
        print(f"\n\n{file}\n{e} -- err\n\n")
        return

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
        isbn_strip = isbn.replace("-", "")
        if len(isbn_strip) in (10, 13):
            print(file)
            print(isbn, "\n")
        # else:
        #     print(file)
        #     print(isbn, "- long", "\n")

    else:
        pass


def main():
    path = "books/"
    api_key = open("apikey.txt", "r").read()

    for file in iglob(f"{path}*.epub"):
        title_epub(file)


if __name__ == "__main__":
    main()
