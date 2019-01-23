import database
import checks
import cache
import guilds
import security
import config
import teams

import uuid

cache = cache.Cache()

emoji_list = ['0⃣', '1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟', '🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵']
emoji_confirm = '✅'
emoji_decline = '❌'

def generate_id():
    return uuid.uuid1().int>>64
