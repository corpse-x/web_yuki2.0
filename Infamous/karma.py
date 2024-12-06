# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX
# https://t.me/O_okarma

# <============================================== IMPORTS =========================================================>
from pyrogram.types import InlineKeyboardButton as ib
from telegram import InlineKeyboardButton

from Mikobot import BOT_USERNAME, OWNER_ID, SUPPORT_CHAT

# <============================================== CONSTANTS =========================================================>
START_IMG = [
"https://telegra.ph/file/b6619541396d150c572a8.jpg",
"https://telegra.ph/file/56c9da084a528eac54142.jpg",
"https://graph.org/file/48903560afb84f882d159.jpg",
"https://graph.org/file/5d4a1cc5a8ae0d4f9fe8d.jpg",
"https://graph.org/file/e2f50154a3ccfaaff275b.jpg",
"https://graph.org/file/87aa0cd80229e67e40180.jpg",
"https://graph.org/file/7817b4a2c2e8191e0dcb5.jpg",
]

HEY_IMG = "https://graph.org/file/7817b4a2c2e8191e0dcb5.jpg"

ALIVE = [
"https://telegra.ph/file/b6619541396d150c572a8.jpg",
"https://telegra.ph/file/56c9da084a528eac54142.jpg",
"https://graph.org/file/48903560afb84f882d159.jpg",
"https://graph.org/file/5d4a1cc5a8ae0d4f9fe8d.jpg",
"https://graph.org/file/e2f50154a3ccfaaff275b.jpg",
"https://graph.org/file/87aa0cd80229e67e40180.jpg",
"https://graph.org/file/7817b4a2c2e8191e0dcb5.jpg",
]
ALIVE_ANIMATION = [
    "https://telegra.ph//file/f9e2b9cdd9324fc39970a.mp4",
    "https://telegra.ph//file/8d4d7d06efebe2f8becd0.mp4",
    "https://telegra.ph//file/c4c2759c5fc04cefd207a.mp4",
    "https://telegra.ph//file/b1fa6609b1c4807255927.mp4",
    "https://telegra.ph//file/f3c7147da6511fbe27c25.mp4",
    "https://telegra.ph//file/39071b73c02e3ff5945ca.mp4",
    "https://telegra.ph//file/8d4d7d06efebe2f8becd0.mp4",
    "https://telegra.ph//file/6efdd8e28756bc2f6e53e.mp4",
]

AFK_IMGS = [

"https://graph.org/file/888a5eaa8bd56e55f28b5.jpg",
"https://graph.org/file/151513db11c93ad5d6aea.jpg",
"https://graph.org/file/786911fbf610009c6e653.jpg",
"https://graph.org/file/93c90aa555f4e9832d563.jpg",
"https://graph.org/file/72397e18d8cbaa590d46d.jpg",
"https://graph.org/file/6cf0959b7676df2364af9.jpg",
"https://graph.org/file/302425f91cd14414b1881.jpg",
"https://graph.org/file/7890aed2cc5a11ef72a12.jpg",
"https://graph.org/file/be7da38e21a7a2b58baa4.jpg",
"https://graph.org/file/6364032206d2c0e7d7641.jpg",
"https://graph.org/file/89cfb8832979558aaa6a6.jpg",
"https://graph.org/file/3aacb2dfa9b9f3bee6ac7.jpg",
"https://graph.org/file/a4d2ef2a8092d4b2cbf57.jpg",
"https://graph.org/file/fe6bf2d7630b51536e39d.jpg",
"https://graph.org/file/971603e9649a99156c2f1.jpg",
"https://graph.org/file/07d24c06d7845b6a392e6.jpg",
"https://graph.org/file/b094bdafdffb7c3bf37da.jpg",
"https://graph.org/file/fa61cc86d951ff00ac943.jpg",
"https://graph.org/file/36fd12d412c59e8cdc870.jpg",
"https://graph.org/file/ee055b3d553837ca1dada.jpg",
"https://graph.org/file/79145769deff07b16584e.jpg",
"https://graph.org/file/2f93f167a73b41df0f634.jpg",
"https://graph.org/file/aa66878529061abb7aab7.jpg",
"https://graph.org/file/f9ee6b486c29e775c2849.jpg",
"https://graph.org/file/99e30c1462483d6946f24.jpg",
"https://graph.org/file/596d850cd780b53c27c74.jpg",
"https://graph.org/file/99edd1b66446e377daff8.jpg",
"https://graph.org/file/4fd1e9d619d449d600b2e.jpg",
"https://graph.org/file/f5f0712bc6e81c1ea99a0.jpg",
"https://graph.org/file/7871bc1236fbf5f936eed.jpg",
"https://graph.org/file/21e3d95a3525b85ecf2be.jpg",
"https://graph.org/file/b07e1016b296921e01979.jpg",
"https://graph.org/file/6f2493edb567825c74c49.jpg",
"https://graph.org/file/034f7d7e051ba29d11f22.jpg",
"https://graph.org/file/21829b55ee68f3dd10f66.jpg",
"https://graph.org/file/a5c3687bc1db9fd06ac41.jpg",
"https://graph.org/file/52db654696dce3d44b545.jpg",
"https://graph.org/file/9ad20cba8c0671663d15d.jpg",
"https://graph.org/file/c79f54af4ee4323ee9aa7.jpg",
"https://graph.org/file/f66af4fb194f6ada367c8.jpg",
"https://graph.org/file/39d70e6bebcb7a95b7e8e.jpg",
"https://graph.org/file/59ca7d31870a60c61fdbf.jpg",
"https://graph.org/file/9ee36c6b1aa28c0f54f9c.jpg",
"https://graph.org/file/ea3a68fff57b8d02f617a.jpg",
"https://graph.org/file/3e3211d88394ad47694d4.jpg",
"https://graph.org/file/68c13d09ee5cca9b5479d.jpg",
"https://graph.org/file/cfc2f89f4e13cac3aff97.jpg",
"https://graph.org/file/8e08202f3299af62ee479.jpg",
"https://graph.org/file/3888300e20e70f79e8ba8.jpg",


"https://graph.org/file/5b2e6ca61047491795136.jpg",
"https://graph.org/file/740339616d692378f027c.jpg",
"https://graph.org/file/51c9284724e28e85ada0c.jpg",
"https://graph.org/file/4b857ba3b38101ed4f216.jpg",
"https://graph.org/file/6308ec539befdf4a335d1.jpg",
"https://graph.org/file/c75324cdc66c8ee5793bb.jpg",
"https://graph.org/file/8caee2c63b2066401e3fa.jpg",
"https://graph.org/file/7d318b2f294e49066e83c.jpg",
"https://graph.org/file/daad921f632f13602d66b.jpg",
"https://graph.org/file/ffca769fa5a991d24c197.jpg",
"https://graph.org/file/4b8dc683c54534c2d72b3.jpg",
"https://graph.org/file/85fe976f1af3a74efa9d3.jpg",
"https://graph.org/file/179f6d3bf8df202691db9.jpg",
"https://graph.org/file/73fe32bb4f1b6f3375e8b.jpg",
"https://graph.org/file/da2323ecba87a8ab4c182.jpg",
"https://graph.org/file/774d0e8bd0327e8e35df0.jpg",
"https://graph.org/file/3d5226b35a97e6c7e6a0e.jpg",
"https://graph.org/file/5fbb1c03db1d8f30856ad.jpg",
"https://graph.org/file/7e1730067ecef12e37652.jpg",
"https://graph.org/file/8b93bce15df14d7225811.jpg",
"https://graph.org/file/b4dd66e242d7661b9dcd2.jpg",
"https://graph.org/file/6efa078b16256a76a1b39.jpg",

"https://graph.org/file/28337379488b8e6af5f54.jpg",
"https://graph.org/file/8c77f65576497f0e3f70d.jpg",
"https://graph.org/file/a1b46e87326e3cf5c868d.jpg",
"https://graph.org/file/606a34cd8f6f454d58378.jpg",
"https://graph.org/file/86390ff86341dbbe98f91.jpg",
"https://graph.org/file/2f68563873477a328ccc2.jpg",
"https://graph.org/file/dbf93aa1c20e4382e64db.jpg",
"https://graph.org/file/7d69d63e399131c050885.jpg",
"https://graph.org/file/602f47667830361f0eb64.jpg",
"https://graph.org/file/777f3ab8abefa835b1059.jpg",
"https://graph.org/file/9beced7d1a18d744cc18a.jpg",
"https://graph.org/file/1867b0db4fcfa20284a6b.jpg",

    "https://graph.org/file/109a941700ce02944afc6.jpg",
    "https://graph.org/file/dd197a3fad2715816528a.jpg",
    "https://graph.org/file/273c4e8811f5249135ae7.jpg",
    "https://graph.org/file/84486beb0429c04806f6c.jpg",
    "https://graph.org/file/609b50e4a4aa03c708247.jpg",
    "https://graph.org/file/6b0a1052c7b64b403a22c.jpg",
    "https://graph.org/file/7ee808520d792c083cdeb.jpg",
    "https://graph.org/file/4db798283a5c3db91c6f6.jpg",
    "https://graph.org/file/bcee30973b23ebd52afcb.jpg",
    "https://graph.org/file/2c402620225d9e117ec54.jpg",
    "https://graph.org/file/7e5229934d9c7858554ab.jpg",
    "https://graph.org/file/adbbf7189416318f40678.jpg",
    "https://graph.org/file/462224ce506163b529e99.jpg",
    "https://graph.org/file/b086290a5c467914d26f6.jpg",
    "https://graph.org/file/df23aa7226f168f2a3a17.jpg",
    "https://graph.org/file/f2ee0e5aa200d8b49a4d1.jpg",
    "https://graph.org/file/d59b342693f4f967de270.jpg",
    "https://graph.org/file/0d10617aa97ece8b7c636.jpg",
    "https://graph.org/file/c37b606a7e940779b7d02.jpg",
    "https://graph.org/file/03a6541f04ad09c048d61.jpg",
    "https://graph.org/file/30696cb28b54f5193e6c4.jpg",
    "https://graph.org/file/d0dd3367dc8cc6db8bd14.jpg",
    "https://graph.org/file/f6effebdf17d142ed52af.jpg",
    "https://graph.org/file/734d7f06f06d892c609fe.jpg",
    "https://graph.org/file/2d6127fef949f898a47ae.jpg",

"https://graph.org/file/7f861f26f80097d869086.jpg",

"https://graph.org/file/07a99f24e310f972c66d6.jpg"
]

FIRST_PART_TEXT = "*FIRST_PART_TEXT* `{}` . . ."

PM_START_TEXT = "* TEST BOT PM_START_TEXT*"

START_BTN = [
    [
        InlineKeyboardButton(
            text="Aᴅᴅ Yᴜᴋɪ !",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="Hᴇʟᴘ", callback_data="extra_command_handler"),
    ],
    [
        InlineKeyboardButton(text="ᴀʙᴏᴜᴛ", callback_data="Miko_"),
#        InlineKeyboardButton(text="SOURCE", callback_data="git_source"),
    ],
    [
        InlineKeyboardButton(text="ᴅᴇᴠ", url=f"tg://user?id={OWNER_ID}"),
    ],
]

GROUP_START_BTN = [
    [
        InlineKeyboardButton(
            text="ʜᴀᴠᴇ ᴍᴇ ɪɴ ᴜʀ ɢᴄ",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="Sᴜᴘᴘᴏʀᴛ ɢᴄ", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton(text="ᴅᴇᴠ-sᴀᴍᴀ", url=f"tg://user?id={OWNER_ID}"),
    ],
]

ALIVE_BTN = [
    [
        ib(text="Nᴇᴛᴡᴏʀᴋ", url="https://t.me/Stern_legion"),
        ib(text="Sᴜᴘᴘᴏʀᴛ", url="https://t.me/yukilogs"),
    ],
    [
        ib(
            text="ɢᴇᴛ ᴍᴇ ɪɴ ᴜʀ ɢᴄ",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

HELP_STRINGS = """
⎋ ꜱᴛᴇᴘ ɪɴᴛᴏ ᴛʜᴇ ʀᴇᴀʟᴍ ᴏꜰ ᴇɴᴅʟᴇꜱꜱ ᴘᴏꜱꜱɪʙɪʟɪᴛɪᴇꜱ—ᴇxᴘʟᴏʀᴇ ᴀʟʟ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅꜱ ᴀᴛ ʏᴏᴜʀ ꜰɪɴɢᴇʀᴛɪᴘꜱ.

╭ᴜɴʟᴇᴀꜱʜ ᴛʜᴇᴍ ᴀʟʟ ᴡɪᴛʜ
╰ /{ᴄᴏᴍᴍᴀɴᴅ}
"""
