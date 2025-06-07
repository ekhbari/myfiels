import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

# قم بتفعيل التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# قائمة القنوات كنص داخل الكود
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
#EXTINF:-1 tvg-id="DijlahTarab.iq",Dijlah Tarab (1080p)
https://ghaasiflu.online/tarab/index.m3u8
#EXTINF:-1 tvg-id="DijlahTV.iq",Dijlah TV (1080p)
https://ghaasiflu.online/Dijlah/index.m3u8
#EXTINF:-1 tvg-id="",Dua Channel (720p)
https://live.ishiacloud.com/haditv.co.uk/dua-channel.m3u8
#EXTINF:-1 tvg-id="GaliKurdistan.iq",Gali Kurdistan (720p) [Not 24/7]
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
#EXTINF:-1 tvg-id="ImamAsrTV.iq",Imam Asr TV (720p)
https://iptv.imamasrtv.com/asrfa/playlist.m3u8
#EXTINF:-1 tvg-id="ImamHusseinTV1.iq",Imam Hussein TV 1 (1080p) [Not 24/7]
https://live.imamhossaintv.com/live/ih1.m3u8
#EXTINF:-1 tvg-id="ImamHusseinTV2.iq",Imam Hussein TV 2 (1080p) [Not 24/7]
https://live.imamhossaintv.com/live/ih2.m3u8
#EXTINF:-1 tvg-id="ImamHusseinTV3.iq",Imam Hussein TV 3 (1080p) [Not 24/7]
https://live.imamhossaintv.com/live/ih3.m3u8
#EXTINF:-1 tvg-id="ImamHusseinTV4.iq",Imam Hussein TV 4 (1080p) [Not 24/7]
https://live.imamhossaintv.com/live/ih4.m3u8
#EXTINF:-1 tvg-id="INews.iq",iNEWS TV (1080p)
https://live.i-news.tv/hls/stream.m3u8
#EXTINF:-1 tvg-id="IshtarTV.iq",Ishtar TV (1080p)
http://ishtar.cdncast.xyz:1935/live/iShtarHD/playlist.m3u8
#EXTINF:-1 tvg-id="KurdChannel.iq",Kurd Channel (480p)
https://kurd-channel.ikoflix.com/hls/stream_2.m3u8
#EXTINF:-1 tvg-id="Kurdistan24.iq",Kurdistan 24 (720p)
https://d1x82nydcxndze.cloudfront.net/live/index.m3u8
#EXTINF:-1 tvg-id="KurdistanTV.iq",Kurdistan TV (720p) [Not 24/7]
https://5a3ed7a72ed4b.streamlock.net/live/SMIL:myStream.smil/playlist.m3u8
#EXTINF:-1 tvg-id="KurdMaxMusic.iq",KurdMax Music (720p)
https://6476e46b58f91.streamlock.net/music/livestream/playlist.m3u8
#EXTINF:-1 tvg-id="KurdMaxShow.iq",KurdMax Show (720p)
https://6476e46b58f91.streamlock.net/liveTrans/SHOW2/playlist.m3u8
#EXTINF:-1 tvg-id="KurdMaxSorani.iq",KurdMax Sorani (1080p)
https://6476e46b58f91.streamlock.net/liveTrans/KurdmaxS0rani!/playlist.m3u8
#EXTINF:-1 tvg-id="Kurdsat.iq",Kurdsat HD
https://kurdsat.akamaized.net/hls/kurdsat.m3u8
#EXTINF:-1 tvg-id="KurdsatNews.iq",Kurdsat News (1080p)
https://kurdsat-news.akamaized.net/hls/kurdsat-news.m3u8
#EXTINF:-1 tvg-id="MarjaeyatTVArabic.iq",Marjaeyat TV Arabic (1080p)
https://livefa.marjaeyattv.com/mtv_ar/playlist.m3u8
#EXTINF:-1 tvg-id="MarjaeyatTVEnglish.iq",Marjaeyat TV English (1080p)
https://livefa.marjaeyattv.com/mtv_en/playlist.m3u8
#EXTINF:-1 tvg-id="MarjaeyatTVPersian.iq",Marjaeyat TV Persian (240p) [Not 24/7]
https://livefa.marjaeyattv.com/mtv_fa/playlist.m3u8
#EXTINF:-1 tvg-id="MBCIraq.iq",MBC Iraq (1080p)
https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-iraq/e38c44b1b43474e1c39cb5b90203691e/index.m3u8
#EXTINF:-1 tvg-id="NRTTV.iq",NRT TV (720p) [Not 24/7]
https://media.streambrothers.com:1936/8226/8226/playlist.m3u8
#EXTINF:-1 tvg-id="NUBARPlusPlus.iq",NUBAR Plus TV (720p)
http://stream.nubar.tv:1935/private/NUBARPlus/playlist.m3u8
#EXTINF:-1 tvg-id="NUBARtv.iq",NUBAR TV (1080p)
http://stream.nubar.tv:1935/private/NUBARtv/playlist.m3u8
#EXTINF:-1 tvg-id="PayamTV.iq",Payam TV (720p) [Not 24/7]
https://media2.streambrothers.com:1936/8218/8218/playlist.m3u8
#EXTINF:-1 tvg-id="RudawTV.iq",Rudaw TV (1080p)
https://svs.itworkscdn.net/rudawlive/rudawlive.smil/playlist.m3u8
#EXTINF:-1 tvg-id="ShamsTV.iq",Shams TV (1080p)
https://stream.shams.tv/hls/stream.m3u8
#EXTINF:-1 tvg-id="UTV.iq",UTV (1080p)
https://mn-nl.mncdn.com/utviraqi2/64c80359/index.m3u8
#EXTINF:-1 tvg-id="WaarTV.iq",Waar TV
https://ca-rt.onetv.app/Waar/index-0.m3u8
#EXTINF:-1 tvg-id="ZagrosTV.iq",Zagros (720p) [Not 24/7]
https://5a3ed7a72ed4b.streamlock.net/zagrostv/SMIL:myStream.smil/playlist.m3u8
#EXTINF:-1 tvg-id="",Zarok TV Sorani (720p)
https://zindisorani.zaroktv.com.tr/hls/stream.m3u8
#EXTINF:-1 tvg-id="AvarTV.iq",Avar TV (1080p)
https://avr.host247.net/live/AvarTv/playlist.m3u8
"""


# قاموس لتخزين القنوات المصنفة: {'Category Name': [{'name': '...', 'url': '...'}, ...]}
categorized_channels = {}

# عدد القنوات في كل صفحة من الأزرار ضمن الفئة
CHANNELS_PER_PAGE = 10

# دالة لتحليل محتوى نص M3U واستخراج وتصنيف القنوات
def parse_m3u_string_with_categories(m3u_string):
    channels_by_category = {}
    if not m3u_string or not m3u_string.strip():
        logger.error("M3U content string is empty.")
        return channels_by_category

    lines = m3u_string.strip().split('\n')

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('#EXTINF'):
            channel_name = "اسم غير معروف"
            channel_url = None
            category = "أخرى" # الفئة الافتراضية
            tvg_id = None

            # استخراج tvg-id واسم القناة
            parts = line.split(',')
            if len(parts) > 1:
                channel_name = parts[-1].strip()
                # البحث عن tvg-id في الجزء الأول
                info_part = parts[0][len('#EXTINF:-1'):].strip()
                if 'tvg-id="' in info_part:
                    id_start = info_part.find('tvg-id="') + len('tvg-id="')
                    id_end = info_part.find('"', id_start)
                    if id_end != -1:
                        tvg_id = info_part[id_start:id_end].strip()

            # تحديد الفئة بناءً على tvg-id (يمكن إضافة المزيد من البلدان هنا)
            if tvg_id:
                if tvg_id.endswith('.iq'):
                    category = "العراق"
                elif tvg_id.endswith('.tr'):
                    category = "تركيا"
                # يمكنك إضافة المزيد من الشروط هنا لتصنيفات أخرى (مثلاً حسب الكلمة في الاسم)
                # elif 'News' in channel_name.lower():
                #     category = "أخبار"

            # البحث عن سطر URL التالي الذي ليس تعليقاً (#) أو فارغاً أو خياراً لـ VLC
            next_line_index = i + 1
            while next_line_index < len(lines) and (lines[next_line_index].strip().startswith('#') or lines[next_line_index].strip() == ''):
                next_line_index += 1

            if next_line_index < len(lines):
                channel_url = lines[next_line_index].strip()
                if channel_url: # تأكد من أن الرابط ليس فارغاً
                     # إضافة القناة إلى الفئة المناسبة
                    if category not in channels_by_category:
                        channels_by_category[category] = []
                    channels_by_category[category].append({'name': channel_name, 'url': channel_url})
                    # logger.info(f"Parsed channel: {channel_name} -> {channel_url} (Category: {category})")
                else:
                     logger.warning(f"Skipping empty URL for channel: {channel_name}")
                i = next_line_index + 1 # ابدأ البحث من السطر التالي بعد URL
            else:
                logger.warning(f"Could not find URL for channel: {channel_name} starting from line {i+1}")
                i += 1 # انتقل للسطر التالي إذا لم يتم العثور على URL
        else:
            i += 1 # انتقل للسطر التالي إذا لم يكن #EXTINF

    # فرز الفئات أبجدياً
    return dict(sorted(channels_by_category.items()))


# تحميل وتصنيف القنوات عند بدء تشغيل السكريبت من النص المضمن
categorized_channels = parse_m3u_string_with_categories(m3u_content)

if not categorized_channels:
    logger.error("No categories or channels loaded from the internal M3U content.")
    print("خطأ: لم يتم تحميل أي قنوات أو فئات من المحتوى المضمن. يرجى التحقق من تنسيق النص في الكود.")


# دالة لإنشاء لوحة مفاتيح inline keyboard للفئات
def get_category_keyboard():
    keyboard = []
    if not categorized_channels:
        return None

    # إضافة زر لكل فئة
    for category_name in categorized_channels.keys():
        # بيانات الـ callback لفتح قنوات هذه الفئة
        callback_data = f'show_category_{category_name}'
        keyboard.append([InlineKeyboardButton(category_name, callback_data=callback_data)])

    # إضافة زر لتحديث القنوات (إذا أردت إضافة هذه الميزة لاحقاً)
    # keyboard.append([InlineKeyboardButton("🔄 تحديث القنوات", callback_data='refresh_channels')])

    return InlineKeyboardMarkup(keyboard)

# دالة لإنشاء لوحة مفاتيح inline keyboard لصفحة معينة من القنوات ضمن فئة محددة
def get_channels_in_category_keyboard(category_name, page=0):
    if category_name not in categorized_channels or not categorized_channels[category_name]:
        # يجب أن لا يحدث هذا إذا كانت الأزرار تنشأ من فئات موجودة
        return None

    channels_in_category = categorized_channels[category_name]
    start_index = page * CHANNELS_PER_PAGE
    end_index = start_index + CHANNELS_PER_PAGE
    current_channels = channels_in_category[start_index:end_index]

    keyboard = []
    # يمكن أن تكون current_channels فارغة إذا كانت الصفحة المطلوبة خارج النطاق الصالح للقنوات
    # لا نرجع None هنا مباشرة للسماح بإضافة زر العودة للفئات

    for index, channel in enumerate(current_channels):
        # بيانات الـ callback لاختيار قناة معينة. تشمل اسم الفئة والفهرس الكلي للقناة في القائمة غير المقسمة والصفحة الحالية
        # الفهرس الكلي ضروري للوصول للقناة الصحيحة من قائمة categorized_channels[category_name]
        channel_global_index = (page * CHANNELS_PER_PAGE) + index # حساب الفهرس الكلي
        # تأكد من أن الفهرس الكلي ضمن النطاق الفعلي لقائمة القنوات في الفئة قبل إنشاء زر له
        if 0 <= channel_global_index < len(channels_in_category):
             # بيانات الـ callback هنا ستكون 'select_channel_<category_name>_<channel_global_index>_<page>'
             # استخدم "_" كفاصل داخل بيانات الـ callback
             callback_data = f'select_channel_{category_name.replace(" ", "_")}_{channel_global_index}_{page}' # استبدل المسافات في اسم الفئة بـ _ لتجنب مشاكل في التحليل اللاحق
             keyboard.append([InlineKeyboardButton(channel['name'], callback_data=callback_data)])
        else:
             logger.warning(f"Attempted to create button for invalid index {channel_global_index} in category {category_name}")


    # إضافة أزرار التنقل بين الصفحات
    navigation_row = []
    # يجب أن يكون هناك قنوات قبل الصفحة الحالية للانتقال للخلف
    if start_index > 0:
        # بيانات الـ callback هنا ستكون 'page_<category_name>_<pagenumber>'
        navigation_row.append(InlineKeyboardButton("<< السابق", callback_data=f'page_{category_name.replace(" ", "_")}_{page - 1}'))
    # يجب أن يكون هناك قنوات بعد الصفحة الحالية للانتقال للأمام
    if end_index < len(channels_in_category):
        # بيانات الـ callback هنا ستكون 'page_<category_name>_<pagenumber>'
        navigation_row.append(InlineKeyboardButton("التالي >>", callback_data=f'page_{category_name.replace(" ", "_")}_{page + 1}'))

    if navigation_row:
        keyboard.append(navigation_row)

    # إضافة زر العودة إلى قائمة الفئات
    keyboard.append([InlineKeyboardButton("🔙 العودة للفئات", callback_data='back_to_categories')])

    if not keyboard: # إذا لم يتم إضافة أي أزرار (القائمة فارغة تماماً)
         # هذا قد يحدث إذا كانت الفئة موجودة لكنها فارغة من القنوات
         return None

    return InlineKeyboardMarkup(keyboard)


# معالج أمر /start
async def start(update: Update, context):
    if not categorized_channels:
         await update.message.reply_text("عذراً، لم يتم تحميل قائمة القنوات. يرجى التحقق من المحتوى المضمن في الكود.")
         return

    reply_markup = get_category_keyboard()
    if reply_markup:
         await update.message.reply_text('مرحباً! اختر فئة قنوات:', reply_markup=reply_markup)
    else:
        # هذا لن يحدث إذا كانت categorized_channels غير فارغة، لكن من الجيد تركه كفحص
        await update.message.reply_text("عذراً، لا توجد فئات قنوات متاحة حالياً.")


# معالج استجابات الـ Callback Query من الأزرار
async def button(update: Update, context):
    query = update.callback_query
    await query.answer() # يجب الرد على الكويري لتجنب ظهور حالة تحميل للمستخدم

    data = query.data
    # logger.info(f"Received callback data: {data}")

    if data == 'back_to_categories':
        # زر العودة من قائمة قنوات الفئة إلى قائمة الفئات الرئيسية
        reply_markup = get_category_keyboard()
        if reply_markup:
            await query.edit_message_text(
                text='اختر فئة قنوات:',
                reply_markup=reply_markup
            )
        else:
            await query.edit_message_text("عذراً، لا توجد فئات قنوات متاحة حالياً.")

    elif data.startswith('show_category_'):
        # المستخدم اختار فئة أو عاد إليها من تفاصيل القناة
        try:
            parts = data.split('_')
            # نتوقع 'show_category_<category_name>_<page_optional>'
            # اسم الفئة يمكن أن يحتوي على مسافات، لذا يجب إعادة بنائه
            # الأجزاء بعد 'show_category' وقبل رقم الصفحة (إذا كان موجوداً) تشكل اسم الفئة
            page = 0
            if len(parts) > 2 and parts[-1].isdigit():
                 page = int(parts[-1])
                 category_name_parts = parts[1:-1]
            else:
                 category_name_parts = parts[1:]
                 page = 0 # الصفحة الافتراضية هي 0 إذا لم يتم تحديدها

            category_name = '_'.join(category_name_parts).replace("_", " ") # إعادة بناء اسم الفئة واستبدال _ بالمسافات

            if category_name in categorized_channels and categorized_channels[category_name]:
                reply_markup = get_channels_in_category_keyboard(category_name, page=page)
                if reply_markup:
                    await query.edit_message_text(
                        text=f'قنوات في فئة "{category_name}" (صفحة {page + 1}):\nاختر قناة:',
                        reply_markup=reply_markup
                    )
                elif page > 0: # إذا كانت الصفحة المطلوبة فارغة ولكنها ليست الصفحة الأولى
                     await query.answer("لا توجد قنوات في هذه الصفحة.") # يمكن تحسين هذا للعودة لآخر صفحة صالحة
                else: # الصفحة 0 فارغة للفئة
                     await query.edit_message_text(f"عذراً، لا توجد قنوات متاحة في فئة \"{category_name}\".")

            else:
                await query.edit_message_text(f"عذراً، الفئة \"{category_name}\" غير موجودة أو فارغة.")

        except (IndexError, ValueError) as e:
             logger.error(f"Error parsing category callback data '{data}': {e}")
             await query.edit_message_text(text="حدث خطأ في معالجة طلبك.")


    elif data.startswith('page_'):
        # المستخدم ضغط على زر السابق/التالي ضمن قائمة قنوات فئة معينة
        try:
            parts = data.split('_')
            # نتوقع الصيغة 'page_<category_name>_<pagenumber>'
            # اسم الفئة يمكن أن يحتوي على مسافات مستبدلة بـ _
            page = int(parts[-1])
            category_name_parts = parts[1:-1]
            category_name = '_'.join(category_name_parts).replace("_", " ") # إعادة بناء اسم الفئة

            if category_name in categorized_channels and categorized_channels[category_name]:
                reply_markup = get_channels_in_category_keyboard(category_name, page)
                if reply_markup:
                    await query.edit_message_text(
                        text=f'قنوات في فئة "{category_name}" (صفحة {page + 1}):\nاختر قناة:',
                        reply_markup=reply_markup
                    )
                else:
                    # إذا كانت الصفحة فارغة، ابق في الصفحة السابقة وأعلم المستخدم
                    await query.answer("لا توجد قنوات أخرى في هذه الصفحة.") # يمكن تحسين هذا للعودة لآخر صفحة صالحة
            else:
                 await query.answer("الفئة غير موجودة.") # لا ينبغي أن يحدث هذا إذا كانت الأزرار تنشأ بشكل صحيح

        except (IndexError, ValueError) as e:
             logger.error(f"Error parsing pagination callback data '{data}': {e}")
             await query.edit_message_text(text="حدث خطأ في معالجة طلب التنقل بين الصفحات.")


    elif data.startswith('select_channel_'):
        # المستخدم اختار قناة من قائمة قنوات فئة معينة
        try:
            parts = data.split('_')
             # نتوقع الصيغة 'select_channel_<category_name>_<channel_global_index>_<page>'
            # اسم الفئة يمكن أن يحتوي على مسافات مستبدلة بـ _
            channel_global_index = int(parts[-2]) # الفهرس الكلي للقناة في قائمة الفئة
            current_page_in_category = int(parts[-1]) # رقم الصفحة التي كان فيها المستخدم داخل الفئة
            # إعادة بناء اسم الفئة من الأجزاء الوسطى
            category_name_parts = parts[2:-2]
            category_name = '_'.join(category_name_parts).replace("_", " ") # اسم الفئة الأصلي

            if category_name in categorized_channels and 0 <= channel_global_index < len(categorized_channels[category_name]):
                channel = categorized_channels[category_name][channel_global_index]
                channel_name = channel['name']
                channel_url = channel['url']

                # إنشاء أزرار: زر لفتح الرابط وزر للعودة لقائمة قنوات الفئة الحالية
                keyboard = [
                    [InlineKeyboardButton(f"▶️ فتح {channel_name} في المشغل", url=channel_url)],
                    # زر العودة يعيد إلى قائمة قنوات الفئة ورقم الصفحة التي كان فيها المستخدم
                    # بيانات الـ callback هنا ستكون 'show_category_CATEGORY_NAME_PAGE'
                    [InlineKeyboardButton("🔙 العودة للقنوات في هذه الفئة", callback_data=f'show_category_{category_name.replace(" ", "_")}_{current_page_in_category}')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.edit_message_text(
                    text=f"لقد اخترت قناة: **{channel_name}**\nاضغط على الزر أدناه للمشاهدة:",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                await query.edit_message_text(text="خطأ: القناة غير موجودة أو الفهرس غير صالح.")
        except (IndexError, ValueError) as e:
             logger.error(f"Error parsing channel selection callback data '{data}': {e}")
             await query.edit_message_text(text="حدث خطأ في معالجة طلبك.")

    # إذا وصل هنا، فهذا يعني أن callback_data غير معالج، قد يحدث لأزرار قديمة
    # logger.warning(f"Unhandled callback data: {data}")


# معالج للرسائل النصية غير الأوامر
async def handle_text(update: Update, context):
    await update.message.reply_text("عذراً، أنا بوت قنوات تلفزيونية. يرجى استخدام الأمر /start لعرض قائمة الفئات.")


# دالة رئيسية لتشغيل البوت
def main():
    # === هام جداً: استبدل 'YOUR_BOT_TOKEN_HERE' برمز البوت الخاص بك ===
    # === لا تشارك هذا الرمز مع أي شخص أو تضعه في مكان عام ===
    bot_token = '8117091320:AAGaBrIeKjkl46PgcdzsK3FP5jFKp9jGzMw' # <-- تم وضع الرمز هنا بناءً على طلبك المسبق. يرجى توخي الحذر!

    if not bot_token: # تحقق إذا كان التوكن لا يزال فارغاً بالخطأ
        logger.error("Bot token is not set.")
        print("\n")
        print("="*50)
        print("!!! خطأ حرج: لم يتم تعيين رمز التوكن (Bot Token) !!!")
        print("يرجى فتح ملف الكود واستبدال النص 'YOUR_BOT_TOKEN_HERE' برمز البوت الخاص بك.")
        print("للحصول على الرمز، تحدث مع BotFather في تليجرام.")
        print("="*50)
        print("\n")
        return

    # تأكد من تحميل القنوات بنجاح من النص المضمن
    if not categorized_channels:
         print("="*50)
         print("!!! تحذير: لم يتم تحميل أي قنوات من المحتوى المضمن !!!")
         print("يرجى التحقق من نص قائمة القنوات المضمن في الكود.")
         print("="*50)
         # قد ترغب في عدم تشغيل البوت إذا لم يتم تحميل أي قنوات
         # return


    application = ApplicationBuilder().token(bot_token).build()

    # إضافة المعالجات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    # معالج للرسائل النصية غير الأوامر (يجب أن يكون بعد معالج الأوامر)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))


    # تشغيل البوت
    logger.info("Bot started polling...")
    print("البوت قيد التشغيل...")
    application.run_polling(timeout=10, stop_signals=None) # أضف timeout و stop_signals لتحسين الإغلاق
    logger.info("Bot stopped.")
    print("تم إيقاف البوت.")


if __name__ == '__main__':
    main()