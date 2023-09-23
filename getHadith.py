import requests


def get_hadith(book_collection: str, book_num: int, hadith_num: int):
    hadith_num = hadith_num - 1

    j = 0
    payload = {"content-type": "application/json"}
    headers = {"x-api-key": "SqD712P3E82xnwOAEOkGd5JZH8s9wRR24TqNFzjk"}
    r = requests.get(
        f"https://api.sunnah.com/v1/collections/{book_collection}/books/{book_num}/hadiths",
        params=payload,
        headers=headers,
    )
    res = r.json()

    for i in res["data"]:

        if j == hadith_num:

            hadith_pt2 = i["hadith"][0]["body"]
            hadith_pt2 = hadith_pt2.replace("<p>", "")
            hadith_pt2 = hadith_pt2.replace("</p>", "")
            hadith_pt3 = i["hadith"][0]["grades"][0]["grade"]
            hadith_pt5 = i["hadith"][1]["body"]
            hadith_pt5 = hadith_pt5.replace("<p>", "")
            hadith_pt5 = hadith_pt5.replace("</p>", "")

            hadith_num = i["hadithNumber"]
            return hadith_pt5, hadith_pt2, hadith_pt3, hadith_num

        else:

            j += 1
