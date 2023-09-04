import urllib.request as request


def google_api_vol_req_generator(
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
        "isbn:": f"{isbn}",
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


def main():
    api_key = open("apikey.txt", "r").read()
    google_api_vol_req_generator(api_key)


if __name__ == "__main__":
    main()
