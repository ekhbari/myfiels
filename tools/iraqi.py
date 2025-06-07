import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import html

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

m3u_content = """
#EXTM3U
#EXTINF:-1 tvg-id="ABNsat.iq",ABNsat (720p)
https://mediaserver.abnvideos.com/streams/abnsat.m3u8
#EXTINF:-1 tvg-id="AfaqTV.iq",Afaq TV
http://63b03f7689049.streamlock.net:1935/live/1/playlist.m3u8
#EXTINF:-1 tvg-id="AfarinBaxcha.iq",Afarin Baxcha (1080p)
https://5dcabf026b188.streamlock.net/afarinTV/livestream/playlist.m3u8
#EXTINF:-1 tvg-id="AfarinTV.iq",Afarin TV (720p) [Not 24/7]
https://65f16f0fdfc51.streamlock.net/afarinTV/livestream/playlist.m3u8
#EXTINF:-1 tvg-id="AlahadTV.iq",Al Ahad TV
http://63b03f7689049.streamlock.net:1935/live/7/playlist.m3u8
#EXTINF:-1 tvg-id="AlAyyamTV.iq",Al Ayyam TV
http://63b03f7689049.streamlock.net:1935/live/6/playlist.m3u8
#EXTINF:-1 tvg-id="AlEshraqTV.iq",Al Eshraq TV
http://63b03f7689049.streamlock.net:1935/live/19/playlist.m3u8
#EXTINF:-1 tvg-id="AlEtejah.iq",Al Etejah TV
http://63b03f7689049.streamlock.net:1935/live/33/playlist.m3u8
#EXTINF:-1 tvg-id="AlghadeerTV.iq",Al Ghadeer TV
http://63b03f7689049.streamlock.net:1935/live/2/playlist.m3u8
#EXTINF:-1 tvg-id="AlIraqia.iq",Al Iraqia (720p)
https://cdn.catiacast.video/abr/8d2ffb0aba244e8d9101a9488a7daa05/playlist.m3u8
#EXTINF:-1 tvg-id="AlIraqiaNews.iq",Al Iraqia News (720p)
https://cdn.catiacast.video/abr/78054972db7708422595bc96c6e024ac/playlist.m3u8
#EXTINF:-1 tvg-id="AlJanoubTV.iq",Al Janoub TV
http://63b03f7689049.streamlock.net:1935/live/18/playlist.m3u8
#EXTINF:-1 tvg-id="AlNujabaTV.iq",Al Nujaba
http://63b03f7689049.streamlock.net:1935/live/3/playlist.m3u8
#EXTINF:-1 tvg-id="AlRabiaaTV.iq" http-referrer="https://player.castr.com/live_c6c4040053cd11ee95b47153d2861736",Al Rabiaa TV (1080p)
#EXTVLCOPT:http-referrer=https://player.castr.com/live_c6c4040053cd11ee95b47153d2861736
https://stream.castr.com/65045e4aba85cfe0025e4a60/live_c6c4040053cd11ee95b47153d2861736/index.fmp4.m3u8
#EXTINF:-1 tvg-id="AlRafidainTV.tr",Al Rafidain (720p) [Not 24/7]
https://arrafidain.tvplayer.online/arrafidaintv/source2/playlist.m3u8
#EXTINF:-1 tvg-id="AlRafidainTV.tr",Al Rafidain (720p) [Not 24/7]
https://arrafidain.tvplayer.online/arrafidaintv/source/playlist.m3u8
#EXTINF:-1 tvg-id="AlRasheedTV.iq",Al Rasheed TV (1080p) [Not 24/7]
https://media1.livaat.com/static/AL-RASHEED-HD/playlist.m3u8
#EXTINF:-1 tvg-id="",Al Shabab TV (1080p)
http://149.100.11.244:8001/play/a07n/index.m3u8
#EXTINF:-1 tvg-id="AlAimmaTV.iq" http-referrer="https://alaimma.tv",Al-Aimma TV (1080p)
#EXTVLCOPT:http-referrer=https://alaimma.tv
http://stream.alaimma.tv/hls/alaimma/h3b1rd584cpq8p60okoj01rnfigdcnia.m3u8
#EXTINF:-1 tvg-id="AlJawadainTV.iq",Al-Jawadain TV (1080p) [Not 24/7]
https://live.aljawadain.org/live/aljawadaintv/playlist.m3u8
#EXTINF:-1 tvg-id="AlNaeemTV.iq",Al-Naeem TV (576p)
https://nl2.livekadeh.com/hls2/alnaeem.m3u8
#EXTINF:-1 tvg-id="AlSharqiya.iq",Al-Sharqiya (1080p)
https://5d94523502c2d.streamlock.net/home/mystream/playlist.m3u8
#EXTINF:-1 tvg-id="AlSharqiyaNews.iq",Al-Sharqiya News (1080p)
https://5d94523502c2d.streamlock.net/alsharqiyalive/mystream/playlist.m3u8
#EXTINF:-1 tvg-id="AlawlaTV.iq",Alawla TV (720p)
https://63b03f7689049.streamlock.net/live/1tv/playlist.m3u8
#EXTINF:-1 tvg-id="AlForatTV.iq",Alforat TV (1080p)
http://95.216.180.111:1935/live/10/playlist.m3u8
#EXTINF:-1 tvg-id="",Alqanat9 TV (1080p)
https://cdn.bestream.io:19360/alqanat9/alqanat9.m3u8
#EXTINF:-1 tvg-id="Alquran.iq",Alquran (1080p)
https://ktvlive.online/stream/hls/ch1.m3u8
#EXTINF:-1 tvg-id="",Althaqalayn TV
http://63b03f7689049.streamlock.net:1935/live/16/playlist.m3u8
#EXTINF:-1 tvg-id="",Althaqalayn TV
http://77.36.160.164:1935/live4/thaghalayn/playlist.m3u8
#EXTINF:-1 tvg-id="AnwarTV2.iq" http-referrer="https://odysee.com/",Anwar TV2 (720p)
#EXTVLCOPT:http-referrer=https://odysee.com/
https://cloud.odysee.live/content/f92670235a1ce2bce4cf77671cc4dcc2188baa1d/master.m3u8
#EXTINF:-1 tvg-id="AnwarTV2.iq",Anwar TV2 (288p)
http://63b03f7689049.streamlock.net:1935/live/13/playlist.m3u8
#EXTINF:-1 tvg-id="AVAFamily.iq",AVA Family
https://ca-rt.onetv.app:8443/AVAFamily/index-0.m3u8
#EXTINF:-1 tvg-id="BayyinatTV.iq",Bayyinat TV (404p)
https://nl2.livekadeh.com/hls2/Bayyinat.m3u8
#EXTINF:-1 tvg-id="BeitolAbbasTVChannel.iq",BeitolAbbas TV Channel (720p)
https://live.beitolabbas.tv/live/beitolabbastv.m3u8
#EXTINF:-1 tvg-id="BeladiSatelliteTV.iq",Beladi Satellite TV (540p)
http://95.216.180.111:1935/live/68/playlist.m3u8
#EXTINF:-1 tvg-id="Channel8.iq",Channel 8 Kurdish (720p)
https://live.channel8.com/Channel8-Kurdish/index.fmp4.m3u8
#EXTINF:-1 tvg-id="Dijlah Tarab.iq",Dijlah Tarab (1080p)
https://ghaasiflu.online/tarab/index.m3u8
#EXTINF:-1 tvg-id="DijlahTV.iq",Dijlah TV (1080p)
https://ghaasiflu.online/Dijlah/index.m3u8
#EXTINF:-1 tvg-id="",Dua Channel (720p)
https://live.ishiacloud.com/haditv.co.uk/dua-channel.m3u8
#EXTINF:-1 tvg-id="Gali Kurdistan.iq",Gali Kurdistan (720p) [Not 24/7]
https://live.bradosti.net/live/GaliKurdistan_playlist.m3u8
#EXTINF:-1 tvg-id="HadiTV3.iq",Hadi TV Azeri and Russian (720p)
https://live.ishiacloud.com/haditv.co.uk/haditv3.m3u8
#EXTINF:-1 tvg-id="HadiTV1.iq",Hadi TV English and Urdu (720p)
https://live.ishiacloud.com/haditv.co.uk/haditv1.m3u8
#EXTINF:-1 tvg-id="HadiTV4.iq",Hadi TV Farsi (720p)
https://live.ishiacloud.com/haditv.co.uk/haditv4.m3u8
#EXTINF:-1 tvg-id="HadiTV5.iq",Hadi TV Hausa (720p)
https://live.ishiacloud.com/haditv.co.uk/haditv5.m3u8
#EXTINF:-1 tvg-id="HadiTV6.iq",Hadi TV Pashto and Persian (720p)
https://live.ishiacloud.com/haditv.co.uk/haditv6.m3u8
#EXTINF:-1 tvg-id="",Hudhud TV
http://63b03f7689049.streamlock.net:1935/live/17/playlist.m3u8
#EXTINF:-1 tvg-id="Imam Asr TV.iq",Imam Asr TV (720p)
https://iptv.imamasrtv.com/asrfa/playlist.m3u8
#EXTINF:-1 tvg-id="Imam Hussein TV 1.iq",Imam Hussein TV 1 (1080p) [Not 24/7]
https://live.imamhossaintv.com/live/ih1.m3u8
#EXTINF:-1 tvg-id="Imam Hussein TV 2.iq",Imam Hussein TV 2 (1080p) [Not 24/7]
https://live.imamhossaintv.com/live/ih2.m3u8
#EXTINF:-1 tvg-id="Imam Hussein TV 3.iq",Imam Hussein TV 3 (1080p) [Not 24/7]
https://live.imamhossaintv.com/live/ih3.m3u8
#EXTINF:-1 tvg-id="Imam Hussein TV 4.iq",Imam Hussein TV 4 (1080p) [Not 24/7]
https://live.imamhossaintv.com/live/ih4.m3u8
#EXTINF:-1 tvg-id="INews.iq",iNEWS TV (1080p)
https://live.i-news.tv/hls/stream.m3u8
#EXTINF:-1 tvg-id="Ishtar TV.iq",Ishtar TV (1080p)
http://ishtar.cdncast.xyz:1935/live/iShtarHD/playlist.m3u8
#EXTINF:-1 tvg-id="Kurd Channel.iq",Kurd Channel (480p)
https://kurd-channel.ikoflix.com/hls/stream_2.m3u8
#EXTINF:-1 tvg-id="Kurdistan 24.iq",Kurdistan 24 (720p)
https://d1x82nydcxndze.cloudfront.net/live/index.m3u8
#EXTINF:-1 tvg-id="Kurdistan TV.iq",Kurdistan TV (720p) [Not 24/7]
https://5a3ed7a72ed4b.streamlock.net/live/SMIL:myStream.smil/playlist.m3u8
#EXTINF:-1 tvg-id="KurdMax Music.iq",KurdMax Music (720p)
https://6476e46b58f91.streamlock.net/music/livestream/playlist.m3u8
#EXTINF:-1 tvg-id="KurdMax Show.iq",KurdMax Show (720p)
https://6476e46b58f91.streamlock.net/liveTrans/SHOW2/playlist.m3u8
#EXTINF:-1 tvg-id="KurdMax Sorani.iq",KurdMax Sorani (1080p)
https://6476e46b58f91.streamlock.net/liveTrans/KurdmaxS0rani!/playlist.m3u8
#EXTINF:-1 tvg-id="Kurdsat.iq",Kurdsat HD
https://kurdsat.akamaized.net/hls/kurdsat.m3u8
#EXTINF:-1 tvg-id="Kurdsat News.iq",Kurdsat News (1080p)
https://kurdsat-news.akamaized.net/hls/kurdsat-news.m3u8
#EXTINF:-1 tvg-id="Marjaeyat TV Arabic.iq",Marjaeyat TV Arabic (1080p)
https://livefa.marjaeyattv.com/mtv_ar/playlist.m3u8
#EXTINF:-1 tvg-id="Marjaeyat TV English.iq",Marjaeyat TV English (1080p)
https://livefa.marjaeyattv.com/mtv_en/playlist.m3u8
#EXTINF:-1 tvg-id="Marjaeyat TV Persian.iq",Marjaeyat TV Persian (240p) [Not 24/7]
https://livefa.marjaeyattv.com/mtv_fa/playlist.m3u8
#EXTINF:-1 tvg-id="MBC Iraq.iq",MBC Iraq (1080p)
https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-iraq/e38c44b1b43474e1c39cb5b90203691e/index.m3u8
#EXTINF:-1 tvg-id="NRT TV.iq",NRT TV (720p) [Not 24/7]
https://media.streambrothers.com:1936/8226/8226/playlist.m3u8
#EXTINF:-1 tvg-id="NUBAR Plus Plus.iq",NUBAR Plus TV (720p)
http://stream.nubar.tv:1935/private/NUBARPlus/playlist.m3u8
#EXTINF:-1 tvg-id="NUBAR tv.iq",NUBAR TV (1080p)
http://stream.nubar.tv:1935/private/NUBARtv/playlist.m3u8
#EXTINF:-1 tvg-id="Payam TV.iq",Payam TV (720p) [Not 24/7]
https://media2.streambrothers.com:1936/8218/8218/playlist.m3u8
#EXTINF:-1 tvg-id="Rudaw TV.iq",Rudaw TV (1080p)
https://svs.itworkscdn.net/rudawlive/rudawlive.smil/playlist.m3u8
#EXTINF:-1 tvg-id="Shams TV.iq",Shams TV (1080p)
https://stream.shams.tv/hls/stream.m3u8
#EXTINF:-1 tvg-id="UTV.iq",UTV (1080p)
https://mn-nl.mncdn.com/utviraqi2/64c80359/index.m3u8
#EXTINF:-1 tvg-id="Waar TV.iq",Waar TV
https://ca-rt.onetv.app/Waar/index-0.m3u8
#EXTINF:-1 tvg-id="Zagros TV.iq",Zagros (720p) [Not 24/7]
https://5a3ed7a72ed4b.streamlock.net/zagrostv/SMIL:myStream.smil/playlist.m3u8
#EXTINF:-1 tvg-id="",Zarok TV Sorani (720p)
https://zindisorani.zaroktv.com.tr/hls/stream.m3u8
#EXTINF:-1 tvg-id="Avar TV.iq",Avar TV (1080p)
https://avr.host247.net/live/AvarTv/playlist.m3u8
"""

channel_translations = {
    "ABNsat (720p)": "قناة ABNsat (720p)",
    "Afaq TV": "قناة آفاق",
    "Afarin Baxcha (1080p)": "قناة أفارين باغجه (1080p)",
    "Afarin TV (720p) [Not 24/7]": "قناة أفارين تي في (720p) [ليست 24/7]",
    "Al Ahad TV": "قناة العهد",
    "Al Ayyam TV": "قناة الأيام",
    "Al Eshraq TV": "قناة الإشراق",
    "Al Etejah TV": "قناة الاتجاه",
    "Al Ghadeer TV": "قناة الغدير",
    "Al Iraqia (720p)": "القناة العراقية (720p)",
    "Al Iraqia News (720p)": "العراقية الإخبارية (720p)",
    "Al Janoub TV": "قناة الجنوب",
    "Al Nujaba": "قناة النجباء",
    "Al Rabiaa TV (1080p)": "قناة الرابعة (1080p)",
    "Al Rafidain (720p) [Not 24/7]": "قناة الرافدين (720p) [ليست 24/7]",
    "Al Rasheed TV (1080p) [Not 24/7]": "قناة الرشيد (1080p) [ليست 24/7]",
    "Al Shabab TV (1080p)": "قناة الشباب (1080p)",
    "Al-Aimma TV (1080p)": "قناة الأئمة (1080p)",
    "Al-Jawadain TV (1080p) [Not 24/7]": "قناة الجوادين (1080p) [ليست 24/7]",
    "Al-Naeem TV (576p)": "قناة النعيم (576p)",
    "Al-Sharqiya (1080p)": "قناة الشرقية (1080p)",
    "Al-Sharqiya News (1080p)": "الشرقية نيوز (1080p)",
    "Alawla TV (720p)": "قناة الأولى (720p)",
    "Alforat TV (1080p)": "قناة الفرات (1080p)",
    "Alqanat9 TV (1080p)": "قناة التاسعة (1080p)",
    "Alquran (1080p)": "قناة القرآن الكريم (1080p)",
    "Althaqalayn TV": "قناة الثقلين",
    "Anwar TV2 (720p)": "قناة أنوار 2 (720p)",
    "Anwar TV2 (288p)": "قناة أنوار 2 (288p)",
    "AVA Family": "قناة AVA Family",
    "Bayyinat TV (404p)": "قناة البينات (404p)",
    "BeitolAbbas TV Channel (720p)": "قناة بيت العباس (720p)",
    "Beladi Satellite TV (540p)": "قناة بلادي الفضائية (540p)",
    "Channel 8 Kurdish (720p)": "قناة Channel 8 الكردية (720p)",
    "Dijlah Tarab (1080p)": "دجلة طرب (1080p)",
    "Dijlah TV (1080p)": "قناة دجلة (1080p)",
    "Dua Channel (720p)": "قناة الدعاء (720p)",
    "Gali Kurdistan (720p) [Not 24/7]": "قناة كلي كردستان (720p) [ليست 24/7]",
    "Hadi TV Azeri and Russian (720p)": "قناة هادي 3 (آذري وروسي) (720p)",
    "Hadi TV English and Urdu (720p)": "قناة هادي 1 (انجليزي وأردو) (720p)",
    "Hadi TV Farsi (720p)": "قناة هادي 4 (فارسي) (720p)",
    "Hadi TV Hausa (720p)": "قناة هادي 5 (هاوسا) (720p)",
    "Hadi TV Pashto and Persian (720p)": "قناة هادي 6 (بشتو وفارسي) (720p)",
    "Hudhud TV": "قناة هدهد",
    "Imam Asr TV (720p)": "قناة الإمام العصر (720p)",
    "Imam Hussein TV 1 (1080p) [Not 24/7]": "قناة الإمام الحسين 1 (1080p) [ليست 24/7]",
    "Imam Hussein TV 2 (1080p) [Not 24/7]": "قناة الإمام الحسين 2 (1080p) [ليست 24/7]",
    "Imam Hussein TV 3 (1080p) [Not 24/7]": "قناة الإمام الحسين 3 (1080p) [ليست 24/7]",
    "Imam Hussein TV 4 (1080p) [Not 24/7]": "قناة الإمام الحسين 4 (1080p) [ليست 24/7]",
    "iNEWS TV (1080p)": "قناة iNEWS (1080p)",
    "Ishtar TV (1080p)": "قناة عشتار (1080p)",
    "Kurd Channel (480p)": "قناة كورد (480p)",
    "Kurdistan 24 (720p)": "كردستان 24 (720p)",
    "Kurdistan TV (720p) [Not 24/7]": "قناة كردستان (720p) [ليست 24/7]",
    "KurdMax Music (720p)": "كورد ماكس ميوزك (720p)",
    "KurdMax Show (720p)": "كورد ماكس شو (720p)",
    "KurdMax Sorani (1080p)": "كورد ماكس سوراني (1080p)",
    "Kurdsat HD": "قناة كوردسات HD",
    "Kurdsat News (1080p)": "كوردسات نيوز (1080p)",
    "Marjaeyat TV Arabic (1080p)": "قناة المرجعية (عربي) (1080p)",
    "Marjaeyat TV English (1080p)": "قناة المرجعية (انجليزي) (1080p)",
    "Marjaeyat TV Persian (240p) [Not 24/7]": "قناة المرجعية (فارسي) (240p) [ليست 24/7]",
    "MBC Iraq (1080p)": "MBC العراق (1080p)",
    "NRT TV (720p) [Not 24/7]": "قناة NRT (720p) [ليست 24/7]",
    "NUBAR Plus TV (720p)": "قناة نوبار بلس (720p)",
    "NUBAR TV (1080p)": "قناة نوبار (1080p)",
    "Payam TV (720p) [Not 24/7]": "قناة پیام (بيام) (720p) [ليست 24/7]",
    "Rudaw TV (1080p)": "قناة رووداو (1080p)",
    "Shams TV (1080p)": "قناة شمس (1080p)",
    "UTV (1080p)": "قناة UTV (1080p)",
    "Waar TV": "قناة وار",
    "Zagros (720p) [Not 24/7]": "قناة زاكروس (720p) [ليست 24/7]",
    "Zarok TV Sorani (720p)": "قناة زاروك (سوراني) (720p)",
    "Avar TV (1080p)": "قناة آفار (1080p)",
}

messages = {
    'en': {
        'choose_language': 'Choose your language:',
        'language_chosen': 'Language set to English. Choose a channel:',
        'choose_channel': 'Choose a channel:',
        'channels_page': 'Channels (page {page}):',
        'selected_channel': 'You selected channel: **{name}**\nClick the button below to watch:',
        'open_in_player': '▶️ Open {name} in Player',
        'back_to_channels': '🔙 Back to Channels',
        'no_channels': 'Sorry, no channels are available.',
        'error_selecting_channel': 'Error: Channel not found or index invalid.',
        'error_pagination': 'Error processing pagination.',
        'error_callback': 'An error occurred processing your request.',
        'unknown_command': 'Sorry, I am a TV channel bot. Use /start to see the channel list.',
        'no_more_pages': 'No more channels on this page.',
        'prev_page': '<< Previous',
        'next_page': 'Next >>',
    },
    'ar': {
        'choose_language': 'اختر لغتك:',
        'language_chosen': 'تم تعيين اللغة إلى العربية. اختر قناة:',
        'choose_channel': 'اختر قناة:',
        'channels_page': 'القنوات (صفحة {page}):',
        'selected_channel': 'لقد اخترت قناة: **{name}**\nاضغط على الزر أدناه للمشاهدة:',
        'open_in_player': '▶️ فتح {name} في المشغل',
        'back_to_channels': '🔙 العودة للقنوات',
        'no_channels': 'عذراً، لا توجد قنوات متاحة حالياً.',
        'error_selecting_channel': 'خطأ: القناة غير موجودة أو الفهرس غير صالح.',
        'error_pagination': 'حدث خطأ في معالجة التنقل بين الصفحات.',
        'error_callback': 'حدث خطأ في معالجة طلبك.',
        'unknown_command': 'عذراً، أنا بوت قنوات تلفزيونية. يرجى استخدام الأمر /start لعرض قائمة القنوات.',
        'no_more_pages': 'لا توجد قنوات أخرى في هذه الصفحة.',
        'prev_page': '<< السابق',
        'next_page': 'التالي >>',
    }
}


channels_list = []

CHANNELS_PER_PAGE = 10

def parse_m3u_string_with_translations(m3u_string, translations):
    channels = []
    if not m3u_string or not m3u_string.strip():
        logger.error("M3U content string is empty.")
        return channels

    lines = m3u_string.strip().split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF'):
            original_name = "اسم غير معروف"
            channel_url = None

            parts = line.split(',')
            if len(parts) > 1:
                original_name = parts[-1].strip()

            next_line_index = i + 1
            while next_line_index < len(lines) and (lines[next_line_index].strip().startswith('#') or lines[next_line_index].strip() == ''):
                next_line_index += 1

            if next_line_index < len(lines):
                channel_url = lines[next_line_index].strip()
                if channel_url:
                    channels.append({
                        'name_en': original_name,
                        'name_ar': translations.get(original_name, original_name),
                        'url': channel_url
                    })
                i = next_line_index + 1
            else:
                logger.warning(f"Could not find URL for channel: {original_name} starting from line {i+1}")
                i += 1
        else:
            i += 1

    return channels

channels_list = parse_m3u_string_with_translations(m3u_content, channel_translations)

if not channels_list:
    logger.error("No channels loaded from the internal M3U content.")
    print("خطأ: لم يتم تحميل أي قنوات من المحتوى المضمن. يرجى التحقق من تنسيق النص في الكود.")


def get_language_keyboard():
    keyboard = [
        [InlineKeyboardButton("English", callback_data='lang_en')],
        [InlineKeyboardButton("العربية", callback_data='lang_ar')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_main_channel_keyboard(page=0, lang='en'):
    if not channels_list:
        return None

    start_index = page * CHANNELS_PER_PAGE
    end_index = start_index + CHANNELS_PER_PAGE
    current_channels = channels_list[start_index:end_index]

    keyboard = []

    for index, channel in enumerate(current_channels):
        channel_name = channel.get(f'name_{lang}', channel['name_en'])

        callback_data = f'select_channel_{start_index + index}_{page}'
        keyboard.append([InlineKeyboardButton(html.escape(channel_name), callback_data=callback_data)])

    navigation_row = []
    if start_index > 0:
        navigation_row.append(InlineKeyboardButton(messages[lang]['prev_page'], callback_data=f'page_{page - 1}'))
    if end_index < len(channels_list):
        navigation_row.append(InlineKeyboardButton(messages[lang]['next_page'], callback_data=f'page_{page + 1}'))

    if navigation_row:
        keyboard.append(navigation_row)

    if not keyboard and page == 0:
         return None

    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context):
    reply_markup = get_language_keyboard()
    await update.message.reply_text(messages['en']['choose_language'] + '\n' + messages['ar']['choose_language'], reply_markup=reply_markup)

async def button(update: Update, context):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data in ['lang_en', 'lang_ar']:
        lang = data.replace('lang_', '')
        context.user_data['lang'] = lang

        if not channels_list:
             await query.edit_message_text(messages[lang]['no_channels'])
             return

        reply_markup = get_main_channel_keyboard(page=0, lang=lang)
        if reply_markup:
             await query.edit_message_text(
                 messages[lang]['language_chosen'],
                 reply_markup=reply_markup
             )
        else:
             await query.edit_message_text(messages[lang]['no_channels'])

    elif data.startswith('page_'):
        lang = context.user_data.get('lang', 'en')
        try:
            page = int(data.replace('page_', ''))

            if page < 0:
                 await query.answer(messages[lang]['no_more_pages'])
                 return

            reply_markup = get_main_channel_keyboard(page, lang)
            if reply_markup:
                 await query.edit_message_reply_markup(reply_markup=reply_markup)
                 # Optionally update text to show page number:
                 # await query.edit_message_text(messages[lang]['channels_page'].format(page=page + 1), reply_markup=reply_markup)
                 await query.answer(messages[lang]['channels_page'].format(page=page + 1))

            elif page > 0:
                 await query.answer(messages[lang]['no_more_pages'])

        except ValueError:
             logger.error(f"Error parsing page number callback data '{data}'")
             await query.answer(messages[lang]['error_pagination'])

    elif data.startswith('select_channel_'):
        lang = context.user_data.get('lang', 'en')
        try:
            parts = data.split('_')
            channel_index = int(parts[2])
            current_page = int(parts[3])

            if 0 <= channel_index < len(channels_list):
                channel = channels_list[channel_index]
                channel_name = channel.get(f'name_{lang}', channel['name_en'])
                channel_url = channel['url']

                keyboard = [
                    [InlineKeyboardButton(messages[lang]['open_in_player'].format(name=html.escape(channel_name)), url=channel_url)],
                    [InlineKeyboardButton(messages[lang]['back_to_channels'], callback_data=f'page_{current_page}')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.edit_message_text(
                    text=messages[lang]['selected_channel'].format(name=html.escape(channel_name)),
                    reply_markup=reply_markup,
                    parse_mode='MarkdownV2'
                )
            else:
                await query.edit_message_text(text=messages[lang]['error_selecting_channel'])
        except (IndexError, ValueError) as e:
             logger.error(f"Error parsing channel selection callback data '{data}': {e}")
             await query.edit_message_text(text=messages[lang]['error_callback'])


async def handle_text(update: Update, context):
    lang = context.user_data.get('lang', 'en')
    await update.message.reply_text(messages[lang]['unknown_command'])

def main():
    bot_token = '8117091320:AAGaBrIeKjkl46PgcdzsK3FP5jFKp9jGzMw'

    if not bot_token:
        logger.error("Bot token is not set.")
        print("\n")
        print("="*50)
        print("!!! CRITICAL ERROR: Bot Token is not set !!!")
        print("Please open the code file and replace 'YOUR_BOT_TOKEN_HERE' with your actual bot token.")
        print("Get your token from BotFather on Telegram.")
        print("="*50)
        print("\n")
        return

    if not channels_list:
         print("="*50)
         print("!!! WARNING: No channels loaded from internal content !!!")
         print("Please check the M3U content string in the code and the parsing function.")
         print("="*50)

    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Bot started polling...")
    print("Bot is running...")
    application.run_polling(timeout=10, stop_signals=None)
    logger.info("Bot stopped.")
    print("Bot stopped.")

if __name__ == '__main__':
    main()