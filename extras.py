import random
from telegram.ext import run_async, Filters
from telegram import Message, Chat, Update, Bot, MessageEntity
from miley import dispatcher
from miley.modules.disable import DisableAbleCommandHandler

ABUSE_STRINGS = (
    "പോടാ പട്ടി",
    "ഡാ പന്നി ",
    "പുന്നാര മോനെ",
    "പോടാ മാക്രി",
    "പോടാ നാറി",
    "വാടാ ... പട്ടീ",
    "പോയി ചാവടാ",
    "നീ പോടാ കാട്ടുകോഴി",
    "പോയി ചത്തൂടെ നിനക്ക്",
    "കോപ്പേ വല്യ ബഹളം വേണ്ട",
    "വല്യ മലരനാണല്ലോടാ നീ",
    "മണ്ണുണ്ണി",
    "ഡാ പന്നക്കിളവ",
    " നിന്റെ കുഞ്ഞമ്മേടെ നായർ",
    "നിന്റെ അപ്പൂപ്പനോട്‌ പോയി പറ",
    "പോ മലരേ",
    "ഇരുട്ട് നിറഞ്ഞ എന്റെ ഈ ജീവിതത്തിലേക്ക് ഒരു തകർച്ചയെ ഓർമ്മിപ്പിക്കാൻ എന്തിന് ഈ ഓട്ടക്കാലണ ആയി നീ വന്നു 😖",
    "നമ്മൾ നമ്മൾ പോലുമറിയാതെ അധോലോകം ആയി മാറിക്കഴിഞ്ഞിരിക്കുന്നു ഷാജിയേട്ടാ...😐",
    "എന്നെ ചീത്ത വിളിക്കു... വേണമെങ്കിൽ നല്ല ഇടി ഇടിക്കു... പക്ഷെ ഉപദേശിക്കരുത്.....😏",
    "ഓ ബ്ലഡി ഗ്രാമവാസീസ്!😡",
    "സീ മാഗ്ഗി ഐ ആം ഗോയിങ് ടു പേ ദി ബിൽ.🤑",
    "പോരുന്നോ എന്റെ കൂടെ!😜",
    "തള്ളെ കലിപ്പ് തീരണില്ലല്ലോ!!🤬",
    "ഞാൻ കണ്ടു...!! കിണ്ടി... കിണ്ടി...!🤣",
    "മോന്തയ്ക്കിട്ട് കൊടുത്തിട്ട് ഒന്ന് എടുത്ത് കാണിച്ചുകൊടുക്ക് അപ്പോൾ കാണും ISI മാർക്ക് 😑",
    "ഡേവീസേട്ട, കിങ്ഫിഷറിണ്ടാ... ചിൽഡ്...! .",
    "പാതിരാത്രിക്ക് നിന്റെ അച്ഛൻ ഉണ്ടാക്കി വെച്ചിരിക്കുന്നോ പൊറോട്ടയും ചിക്കനും....😬",
    "ഇത് ഞങ്ങളുടെ പണിസാധനങ്ങളാ രാജാവേ.🔨⛏",
    "കളിക്കല്ലേ കളിച്ചാൽ ഞാൻ തീറ്റിക്കുമെ പുളിമാങ്ങ....😎",
    "മ്മക്ക് ഓരോ ബിയറാ കാച്ചിയാലോ...🥂",
    "ഓ പിന്നെ നീ ഒക്കെ പ്രേമിക്കുമ്പോൾ അത് പ്രണയം.... നമ്മൾ ഒക്കെ പ്രേമിക്കുമ്പോൾ അത് കമ്പി...😩",
    "കള്ളടിക്കുന്നവനല്ലേ കരിമീനിന്റെ സ്വാദറിയു.....😋",
    "ഡാ വിജയാ നമുക്കെന്താ ഈ ബുദ്ധി നേരത്തെ തോന്നാതിരുന്നത്...!🙄",
    "ഇത്രേം കാലം എവിടെ ആയിരുന്നു....!🥰",
    "ദൈവമേ എന്നെ മാത്രം രക്ഷിക്കണേ....⛪",
    "എനിക്കറിയാം ഇവന്റെ അച്ഛന്റെ പേര് ഭവാനിയമ്മ എന്നാ....😂🤣🤣",
    "ഡാ ദാസാ... ഏതാ ഈ അലവലാതി.....😒",
    "ഉപ്പുമാവിന്റെ ഇംഗ്ലീഷ് സാൾട് മംഗോ ട്രീ.....🤔",
    "മക്കളെ.. രാജസ്ഥാൻ മരുഭൂമിയിലേക്ക് മണല് കയറ്റിവിടാൻ നോക്കല്ലേ.....🥵",
    "നിന്റെ അച്ഛനാടാ പോൾ ബാർബർ....🤒",
    "കാർ എൻജിൻ ഔട്ട് കംപ്ലീറ്റ്‌ലി.....🥵",
    "ഇത് കണ്ണോ അതോ കാന്തമോ...👀",
    "നാലാമത്തെ പെഗ്ഗിൽ ഐസ്‌ക്യൂബ്സ് വീഴുന്നതിനു മുൻപ് ഞാൻ അവിടെ എത്തും.....😉",
    "അവളെ ഓർത്ത് കുടിച്ച കല്ലും നനഞ്ഞ മഴയും വേസ്റ്റ്....💔",
    "എന്നോട് പറ ഐ ലവ് യൂ ന്ന്....😘",
    "അല്ല ഇതാര് വാര്യംപിള്ളിയിലെ മീനാക്ഷി അല്ലയോ... എന്താ മോളെ സ്കൂട്ടറില്....🙈 "
  )

SONG_STRINGS = (
    "🎶 മിഴിയറിയാതെ വന്നു നീ മിഴിയൂഞ്ഞാലിൽ... കനവറിയാതെയേതോ കിനാവു പോലെ... 🎶.",
    "🎶 നിലാവിന്റെ നീലഭസ്മ കുറിയണിഞ്ഞവളേ... കാതിലോലക്കമ്മലിട്ടു കുണുങ്ങി നിന്നവളേ... 🎶",
    "🎶 എന്തിനു വേറൊരു സൂര്യോദയം... നീയെൻ പൊന്നുഷസ്സന്ധ്യയല്ലേ... 🎶", 
    "🎶 ശ്രീരാഗമോ തേടുന്നിതെൻ വീണതൻ പൊൻ തന്ത്രിയിൽ... 🎶", 
    "🎶 മഴത്തുള്ളികൾ പൊഴിഞ്ഞീടുമീ നാടൻ വഴി... നനഞ്ഞോടിയെൻ കുടക്കീഴിൽ നീ വന്ന നാൾ... 🎶", 
    "🎶 നീയൊരു പുഴയായ് തഴുകുമ്പോൾ ഞാൻ പ്രണയം വിടരും കരയാവും... 🎶", 
    "🎶 അല്ലിമലർ കാവിൽ പൂരം കാണാൻ... അന്നു നമ്മൾ പോയി രാവിൽ നിലാവിൽ... 🎶", 
    "🎶 നിലാവിന്റെ നീലഭസ്മ കുറിയണിഞ്ഞവളേ... കാതിലോലക്കമ്മലിട്ടു കുണുങ്ങി നിന്നവളേ... 🎶", 
    "🎶 ചന്ദനച്ചോലയിൽ മുങ്ങിനീരാടിയെൻ ഇളമാൻ കിടാവേ ഉറക്കമായോ... 🎶", 
    "🎶 അന്തിപ്പൊൻവെട്ടം കടലിൽ മെല്ലെത്താഴുമ്പോൾ... മാനത്തെ മുല്ലത്തറയില് മാണിക്യച്ചെപ്പ്... 🎶", 
    "🎶 താമരപ്പൂവിൽ വാഴും ദേവിയല്ലോ നീ... പൂനിലാക്കടവിൽ പൂക്കും പുണ്യമല്ലോ നീ... 🎶", 
    "🎶 കുന്നിമണിച്ചെപ്പു തുറന്നെണ്ണി നോക്കും നേരം, പിന്നിൽവന്നു കണ്ണു പൊത്തും കള്ളനെങ്ങു പോയി... 🎶", 
    "🎶 ശ്യാമാംബരം പുൽകുന്നൊരാ വെൺചന്ദ്രനായ് നിൻ പൂമുഖം... 🎶", 
    "🎶 പാടം പൂത്തകാലം പാടാൻ വന്നു നീയും... 🎶", 
    "🎶 കറുകവയൽ കുരുവീ... മുറിവാലൻ കുരുവീ... തളിർ വെറ്റിലയുണ്ടോ... വരദക്ഷിണ വെക്കാൻ... 🎶", 
    "🎶 പത്തുവെളുപ്പിന് മുറ്റത്തു നിക്കണ കസ്തൂരി മുല്ലയ്ക്ക് കാത്തുകുത്ത്... എന്റെ കസ്തൂരി മുല്ലയ്ക്ക് കാതു കുത്ത്.. 🎶", 
    "🎶 മഞ്ഞൾ പ്രസാദവും നെറ്റിയിൽ ചാർത്തി... മഞ്ഞക്കുറിമുണ്ടു ചുറ്റി... 🎶", 
    "🎶 കറുത്തപെണ്ണേ നിന്നെ കാണാഞ്ഞിട്ടൊരു നാളുണ്ടേ... 🎶"
 )

@run_async
def abuse(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(ABUSE_STRINGS))
    else:
      message.reply_text(random.choice(ABUSE_STRINGS))

@run_async
def sing(bot: Bot, update: Update):
    bot.sendChatAction(update.effective_chat.id, "typing") # Bot typing before send messages
    message = update.effective_message
    if message.reply_to_message:
      message.reply_to_message.reply_text(random.choice(SONG_STRINGS))
    else:
      message.reply_text(random.choice(SONG_STRINGS))

__help__ = """
- /abuse : Abuse someone in malayalam.
- /sing : First lines of some random malayalam Songs.
"""

__mod_name__ = "Extras"

ABUSE_HANDLER = DisableAbleCommandHandler("abuse", abuse)
SING_HANDLER = DisableAbleCommandHandler("sing", sing)

dispatcher.add_handler(ABUSE_HANDLER)
dispatcher.add_handler(SING_HANDLER)
