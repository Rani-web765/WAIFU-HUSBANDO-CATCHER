class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "7526369190"
    sudo_users = "7526369190", "5884969921", "6961287189"
    GROUP_ID = -1002133191051
    TOKEN = "6462620320:AAGIBSjD_PmyiSNPmF3kdYsO0G2TSMpQe9M"
    mongo_url = "mongodb+srv://Srikanta:srikanta@cluster0.xzbil3m.mongodb.net/?retryWrites=true&w=majority"
    PHOTO_URL = ["https://telegra.ph/file/ed23556d07d33db18402d.jpg", "https://telegra.ph//file/e64337bbc6cdac7e6b178.jpg"]
    SUPPORT_CHAT = "waifexanime"
    UPDATE_CHAT = "waifexanime"
    BOT_USERNAME = "Collectionwaife_bot"
    CHARA_CHANNEL_ID = "-1002119873436"
    api_id = 26626068
    api_hash = "bf423698bcbe33cfd58b11c78c42caa2"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
