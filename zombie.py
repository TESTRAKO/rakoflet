import pygame
import random
import math
from pygame.locals import *
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import time

# تهيئة pygame
pygame.init()

# إعداد نافذة اللعبة
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("لعبة النجاة من الزومبي")

# تحميل الصور مع التحقق
try:
    background = pygame.image.load("madina.png")
    player_img = pygame.image.load("ptl.png")
    zombie_img = pygame.image.load("zombi.png")
except Exception as e:
    print(f"خطأ في تحميل الملفات: {e}")
    exit()

# إعدادات اللاعب
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT // 2
player_speed = 5

# إعدادات الزومبي
zombie_width, zombie_height = 50, 50
zombie_speed = 1
zombies = [{"x": random.randint(0, WIDTH - zombie_width), "y": random.randint(0, HEIGHT - zombie_height)} for _ in range(5)]

# تحميل الصوتيات
try:
    pygame.mixer.init()
    bg_music = pygame.mixer.Sound("muic (online-audio-converter.com).wav")
    bg_music.play(-1)  # تكرار الموسيقى
except Exception as e:
    print(f"خطأ في تحميل الصوتيات: {e}")

# تحميل الخط
try:
    font = pygame.font.Font("arial.ttf", 36)  # استخدام الخط الجديد
except Exception as e:
    print(f"خطأ في تحميل الخط: {e}")
    exit()

# دالة لإعادة تشكيل النصوص العربية
def render_text_arabic(text, font, color, x, y):
    reshaped_text = reshape(text)
    bidi_text = get_display(reshaped_text)
    text_surface = font.render(bidi_text, True, color)
    window.blit(text_surface, (x, y))

# دالة لطباعة النصوص ببطء مع الانتظار حتى الضغط على "Enter"
def slow_print(text, color, delay=0.05):
    reshaped_text = reshape(text)
    bidi_text = get_display(reshaped_text)
    text_surface = font.render(bidi_text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

    for i in range(len(bidi_text)):
        surface = font.render(bidi_text[:i + 1], True, color)
        window.fill((0, 0, 0))  # تنظيف الشاشة
        window.blit(surface, text_rect)
        pygame.display.update()
        time.sleep(delay)

    # الانتظار حتى يضغط المستخدم على "Enter"
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN:  # عندما يضغط المستخدم على "Enter"
                    waiting_for_input = False

# وظيفة لعرض المقدمة
def display_intro():
    render_text_arabic("لعبة النجاة من الزومبي", font, (255, 0, 0), WIDTH // 2 - 150, 100)
    slow_print("مرحباً بك في هذه اللعبة الشيقة!", (255, 255, 255), 0.05)
    slow_print("لقد انتشر وباء الزومبي في العالم، وعليك النجاة.", (255, 255, 255), 0.05)
    slow_print("خياراتك ستحدد مصيرك. هل ستنجو أم ستسقط؟", (255, 0, 0), 0.05)
    slow_print("اختر بحكمة!", (255, 255, 255), 0.05)

# دالة لاختيار التصرفات باستخدام لوحة المفاتيح
def choose_action(question, option1, option2):
    choice = None
    while choice is None:
        window.fill((0, 0, 0))
        render_text_arabic(question, font, (255, 255, 255), WIDTH // 2 - 200, HEIGHT // 2 - 100)
        render_text_arabic(f"(1): {option1}", font, (255, 255, 255), WIDTH // 2 - 200, HEIGHT // 2)
        render_text_arabic(f"(2): {option2}", font, (255, 255, 255), WIDTH // 2 - 200, HEIGHT // 2 + 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_1:
                    choice = "1"
                elif event.key == K_2:
                    choice = "2"
    
    return choice

# بداية اللعبة
display_intro()

# المرحلة الأولى
first_choice = choose_action("سمعت صوت غريب خارج المنزل", "تختبئ في المنزل", "تبحث عن الصوت مثل الشجاع")

if first_choice == "1":
    slow_print("قررت البقاء مختبئًا ولكن الزومبي سمعوا خطواتك ودخلوا.", (255, 0, 0), 0.05)
elif first_choice == "2":
    slow_print("رأوك وكسروا الباب ودخلوا عليك.", (255, 0, 0), 0.05)

# المرحلة الثانية
second_choice = choose_action("هل ستواجه الزومبي؟", "تقاتلهم", "تهرب من النافذة")

if second_choice == "1":
    slow_print("حاولت القتال ولكن عددهم كان كبيرًا وقتلوك.", (255, 0, 0), 0.05)
    slow_print("انتهت اللعبة. حاول مجددًا.", (255, 0, 0), 0.05)
elif second_choice == "2":
    slow_print("قفزت من النافذة وهربت.", (0, 255, 0), 0.05)

    # المرحلة الثالثة
    third_choice = choose_action("ماذا تفعل الآن؟", "تذهب لمكان آمن", "تعود لقتل الزومبي")

    if third_choice == "1":
        slow_print("هربت ووجدت مكانًا آمنًا.", (0, 0, 255), 0.05)
    elif third_choice == "2":
        slow_print("عدت وقتلت الزومبي لكنك أُصبت.", (0, 255, 255), 0.05)

# نهاية اللعبة
slow_print("انتهت اللعبة. ترقب الجزء الثاني!", (0, 255, 0), 0.05)
