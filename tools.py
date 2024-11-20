import shortuuid

ARTIST_LINK = {}
ALBUM_LINK = {}
SONG_LINK = {}
KIND_LINK = {}

def getUUID():
    su = shortuuid.ShortUUID(alphabet="1234567890")
    return su.random(length=8)


def formatLine(line:str):
    return line.strip().replace(" ","_")