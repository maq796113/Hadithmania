import html2text
import aiohttp
import settings
import arabic_reshaper

logger = settings.logging.getLogger("bot")


async def get_hadith(book_collection: str, book_num: int, hadith_num: int):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_tables = True

    payload = {"content-type": "application/json"}
    headers = {"x-api-key": settings.HADITH_API_TOKEN}
    
    url = f"https://api.sunnah.com/v1/collections/{book_collection}/books/{book_num}/hadiths/{hadith_num}"
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload, headers=headers, timeout=10) as response:
                if response.status != 200:
                    logger.error(f"API returned status {response.status}")
                    return None
                data = await response.json()

        hadith_chap_title_eng = data["hadith"][0]["chapterTitle"]

        hadith_eng = h.handle(data["hadith"][0]["body"]).replace("\n", "")

        if data["hadith"][0]["grades"]:
            grading = data["hadith"][0]["grades"][0]["grade"]
        else:
            grading = data["hadith"][1]["grades"][0]["grade"] + f"({data['hadith'][1]['grades'][0]['graded_by']})"

        hadith_chap_title_ar = data["hadith"][1]["chapterTitle"]

        hadith_ar = h.handle(data["hadith"][1]["body"]).replace("\n", "").replace("‏.‏", "")
        reshaped_hadith_ar = arabic_reshaper.reshape(hadith_ar)

        hadith_num_str = data["hadithNumber"]
        chapter_num = data["chapterId"].replace(".00", "")

        if '\"' in hadith_eng:
            hadith_eng = put_asterisk_in_quotes(hadith_eng)

        return (
            reshaped_hadith_ar,
            hadith_eng,
            grading,
            hadith_num_str,
            hadith_chap_title_eng,
            hadith_chap_title_ar,
            chapter_num
        )
    except Exception as e:
        logger.error(f"Error in get_hadith: {str(e)}")
        return None


def put_asterisk_in_quotes(text: str) -> str:
    words = text.split()

    for i, word in enumerate(words):
        if word[0] == '\"':
            words[i] = words[i].replace('\"', '**\"')

        if word[-1] == '\"':
            words[i] = words[i].replace('\"', '\"**')

    return ' '.join(words)
