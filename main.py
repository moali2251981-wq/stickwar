import pygame
import random
import math
import sys
import itertools
import json

# ================= ================= =================
# 1. التهيئة الأساسية وإعداد الشاشة للموبايل
# ================= ================= =================
pygame.init()
pygame.font.init()
pygame.mixer.init()

info = pygame.display.Info()
W, H = info.current_w, info.current_h
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Stick War Ultra Mobile")
clock = pygame.time.Clock()

SCALE = max(0.75, min(2.6, min(W, H) / 900))

def S(v):
    return max(1, int(v * SCALE))

# ================= ================= =================
# 2. الألوان والخطوط والأشكال ونظام الأصوات البسيط والآمن
# ================= ================= =================
GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
GOLD = (241, 196, 15)
GRAY = (80, 80, 80)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRASS = (58, 158, 73)
DARK_GRASS = (40, 110, 50)
NEUTRAL = (180, 180, 180)
PURPLE = (155, 89, 182)
CYAN = (52, 224, 219)

font_s = pygame.font.Font(None, S(18))
font_m = pygame.font.Font(None, S(24))
font_b = pygame.font.Font(None, S(36))
font_big = pygame.font.Font(None, S(50))

TREES = [(random.randint(0, W), random.randint(0, H), S(12)) for _ in range(50)]

def draw_bg(shake=0):
    sx = random.randint(-shake, shake) if shake > 0 else 0
    sy = random.randint(-shake, shake) if shake > 0 else 0
    screen.fill(GRASS)
    for x, y, r in TREES:
        pygame.draw.circle(screen, DARK_GRASS, (x + sx, y + sy), r)

# نظام أصوات آمن وبسيط لا يسبب شاشة سوداء
SOUNDS = {}

def play_sfx(name):
    if SAVE.get("muted", False):
        return
    try:
        if name in SOUNDS and SOUNDS[name] is not None:
            SOUNDS[name].play()
    except Exception:
        pass

TROOPS = {
    "WARRIOR":  {"cost": 20,  "hp": 3,  "speed": 3.2, "r": S(7),  "dmg": 6},
    "TANK":     {"cost": 120, "hp": 15, "speed": 1.7, "r": S(14), "dmg": 14},
    "ARCHER":   {"cost": 45,  "hp": 2,  "speed": 2.6, "r": S(6),  "dmg": 3,  "ranged": True, "range": S(130), "cd": 45},
    "SPEARMAN": {"cost": 35,  "hp": 4,  "speed": 2.8, "r": S(8),  "dmg": 5,  "ranged": True, "range": S(100), "cd": 40},
    "MAGE":     {"cost": 80,  "hp": 5,  "speed": 2.2, "r": S(9),  "dmg": 12, "ranged": True, "range": S(140), "cd": 60},
    "GIANT":    {"cost": 200, "hp": 30, "speed": 1.2, "r": S(18), "dmg": 22},
}
TROOP_KEYS = list(TROOPS.keys())
BONUS = 0

SAVE = {
    "gems": 0,
    "best_free_money": 0, 
    "zones_conquered": 0, 
    "best_streak": 0, 
    "current_streak": 0,
    "map_owners": ["player", "enemy", "enemy"],
    "music_vol": 0.8,
    "sfx_vol": 0.8,
    "muted": False
}

def load_save():
    global SAVE
    try:
        with open("stickwar_save.json", "r") as f:
            data = json.load(f)
            SAVE.update(data)
    except Exception:
        pass

def write_save():
    try:
        with open("stickwar_save.json", "w") as f:
            json.dump(SAVE, f)
    except Exception:
        pass

def apply_audio_settings():
    try:
        vol = 0.0 if SAVE["muted"] else SAVE["music_vol"]
        pygame.mixer.music.set_volume(vol)
    except Exception:
        pass

load_save()
apply_audio_settings()
# ================= ================= =================
# 4. الشاشات المساعدة والإعدادات والمتجر والتعليمات
# ================= ================= =================
def result_screen(msg, sub, color):
    if color == GREEN:
        play_sfx("win")
    else:
        play_sfx("lose")
        
    t0 = pygame.time.get_ticks()
    while pygame.time.get_ticks() - t0 < 2500:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                return
        screen.fill(BLACK)
        t = font_big.render(msg, True, color)
        screen.blit(t, (W // 2 - t.get_width() // 2, H // 2 - S(60)))
        s = font_m.render(sub, True, WHITE)
        screen.blit(s, (W // 2 - s.get_width() // 2, H // 2 + S(10)))
        pygame.display.flip()
        clock.tick(60)

def simulate_ad():
    play_sfx("click")
    t0 = pygame.time.get_ticks()
    duration = 2000
    while pygame.time.get_ticks() - t0 < duration:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((10, 10, 25))
        remaining = max(1, int((duration - (pygame.time.get_ticks() - t0)) / 1000) + 1)
        
        ad_title = font_big.render("📺 REWARDED AD PLAYING...", True, GOLD)
        screen.blit(ad_title, (W // 2 - ad_title.get_width() // 2, H // 2 - S(40)))
        
        timer_txt = font_m.render(f"Reward in: {remaining}s", True, WHITE)
        screen.blit(timer_txt, (W // 2 - timer_txt.get_width() // 2, H // 2 + S(20)))
        
        pygame.display.flip()
        clock.tick(60)

def show_tutorial():
    play_sfx("click")
    instructions = [
        "--- HOW TO PLAY ---",
        "",
        "1. RECRUIT: Select a unit from the right side shop.",
        "2. ATTACK: Tap enemy castle directly to attack it.",
        "3. DEFEND: Tap your castle to create a smart defense line.",
        "4. ZONES: Tap circular zones to send troops to capture them.",
        "5. GOLD CRATES: Tap gold crates on field for extra gold.",
        "6. CONTROLS: Use bottom buttons or screen taps to control target.",
        "",
        "[ TAP ANYWHERE ON SCREEN TO CLOSE ]"
    ]
    pygame.event.clear()
    while True:
        draw_bg()
        overlay = pygame.Surface((W - S(40), H - S(40)))
        overlay.set_alpha(230)
        overlay.fill(BLACK)
        screen.blit(overlay, (S(20), S(20)))
        pygame.draw.rect(screen, GOLD, (S(20), S(20), W - S(40), H - S(40)), width=S(3), border_radius=S(15))
        
        y = S(45)
        for line in instructions:
            if line.startswith("---"):
                txt = font_b.render(line, True, GOLD)
            elif line.startswith("["):
                txt = font_b.render(line, True, GREEN)
            else:
                txt = font_m.render(line, True, WHITE)
            screen.blit(txt, (W // 2 - txt.get_width() // 2, y))
            y += S(30)

        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                return
        clock.tick(60)

def settings_screen():
    global SAVE
    bw, bh = S(40), S(40)
    
    back_btn = pygame.Rect(S(15), S(10), S(90), S(35))
    music_down = pygame.Rect(W // 2 + S(20), S(110), bw, bh)
    music_up = pygame.Rect(W // 2 + S(210), S(110), bw, bh)
    sfx_down = pygame.Rect(W // 2 + S(20), S(180), bw, bh)
    sfx_up = pygame.Rect(W // 2 + S(210), S(180), bw, bh)
    mute_btn = pygame.Rect(W // 2 - S(100), S(250), S(200), S(45))

    while True:
        draw_bg()
        pygame.draw.rect(screen, BLACK, (0, 0, W, S(55)))
        
        t = font_b.render("SETTINGS ⚙️", True, CYAN)
        screen.blit(t, (W // 2 - t.get_width() // 2, S(12)))

        m_txt = font_m.render(f"Music Vol: {int(SAVE['music_vol'] * 100)}%", True, WHITE)
        screen.blit(m_txt, (W // 2 - S(200), S(120)))
        pygame.draw.rect(screen, RED, music_down, border_radius=S(5))
        pygame.draw.rect(screen, GREEN, music_up, border_radius=S(5))
        screen.blit(font_b.render("-", True, WHITE), (music_down.centerx - S(5), music_down.centery - S(12)))
        screen.blit(font_b.render("+", True, WHITE), (music_up.centerx - S(7), music_up.centery - S(12)))

        s_txt = font_m.render(f"SFX Vol: {int(SAVE['sfx_vol'] * 100)}%", True, WHITE)
        screen.blit(s_txt, (W // 2 - S(200), S(190)))
        pygame.draw.rect(screen, RED, sfx_down, border_radius=S(5))
        pygame.draw.rect(screen, GREEN, sfx_up, border_radius=S(5))
        screen.blit(font_b.render("-", True, WHITE), (sfx_down.centerx - S(5), sfx_down.centery - S(12)))
        screen.blit(font_b.render("+", True, WHITE), (sfx_up.centerx - S(7), sfx_up.centery - S(12)))

        m_col = RED if SAVE["muted"] else GREEN
        pygame.draw.rect(screen, m_col, mute_btn, border_radius=S(10))
        mute_txt = font_m.render("SOUND: OFF 🔇" if SAVE["muted"] else "SOUND: ON 🔊", True, WHITE)
        screen.blit(mute_txt, (mute_btn.centerx - mute_txt.get_width() // 2, mute_btn.centery - mute_txt.get_height() // 2))

        pygame.draw.rect(screen, RED if back_btn.collidepoint(pygame.mouse.get_pos()) else (120, 40, 40), back_btn, border_radius=S(8))
        back_txt = font_s.render("< MENU", True, WHITE)
        screen.blit(back_txt, (back_btn.centerx - back_txt.get_width() // 2, back_btn.centery - back_txt.get_height() // 2))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                play_sfx("click")
                if back_btn.collidepoint(e.pos):
                    write_save()
                    return
                if music_down.collidepoint(e.pos):
                    SAVE["music_vol"] = max(0.0, round(SAVE["music_vol"] - 0.1, 1))
                    apply_audio_settings()
                if music_up.collidepoint(e.pos):
                    SAVE["music_vol"] = min(1.0, round(SAVE["music_vol"] + 0.1, 1))
                    apply_audio_settings()
                if sfx_down.collidepoint(e.pos):
                    SAVE["sfx_vol"] = max(0.0, round(SAVE["sfx_vol"] - 0.1, 1))
                if sfx_up.collidepoint(e.pos):
                    SAVE["sfx_vol"] = min(1.0, round(SAVE["sfx_vol"] + 0.1, 1))
                if mute_btn.collidepoint(e.pos):
                    SAVE["muted"] = not SAVE["muted"]
                    apply_audio_settings()
        clock.tick(60)

def gems_shop():
    global BONUS, SAVE
    play_sfx("click")
    bw, bh = S(300), S(45)
    
    back_btn = pygame.Rect(S(15), S(10), S(90), S(35))
    ad_btn = pygame.Rect(W // 2 - bw // 2, S(70), bw, bh)
    
    packages = [
        {"gems": 10,  "gold": 200,  "rect": pygame.Rect(W // 2 - bw // 2, S(130), bw, bh)},
        {"gems": 50,  "gold": 1200, "rect": pygame.Rect(W // 2 - bw // 2, S(185), bw, bh)},
        {"gems": 100, "gold": 2800, "rect": pygame.Rect(W // 2 - bw // 2, S(240), bw, bh)},
        {"gems": 200, "gold": 6000, "rect": pygame.Rect(W // 2 - bw // 2, S(295), bw, bh)},
    ]
    
    msg_time = 0
    msg_text = ""

    while True:
        draw_bg()
        pygame.draw.rect(screen, BLACK, (0, 0, W, S(55)))
        
        t = font_b.render("GEM SHOP 💎", True, CYAN)
        screen.blit(t, (W // 2 - t.get_width() // 2, S(12)))
        
        gems_txt = font_m.render(f"GEMS: {SAVE['gems']} 💎 | BONUS: +${BONUS}", True, GOLD)
        screen.blit(gems_txt, (W - gems_txt.get_width() - S(15), S(15)))

        pygame.draw.rect(screen, PURPLE if ad_btn.collidepoint(pygame.mouse.get_pos()) else (100, 40, 140), ad_btn, border_radius=S(10))
        atxt = font_m.render("📺 WATCH AD (+10 💎)", True, WHITE)
        screen.blit(atxt, (ad_btn.centerx - atxt.get_width() // 2, ad_btn.centery - atxt.get_height() // 2))

        for pkg in packages:
            r = pkg["rect"]
            hover = r.collidepoint(pygame.mouse.get_pos())
            pygame.draw.rect(screen, GREEN if hover else (40, 120, 40), r, border_radius=S(10))
            ptxt = font_s.render(f"BUY +${pkg['gold']} GOLD  ({pkg['gems']} 💎)", True, WHITE)
            screen.blit(ptxt, (r.centerx - ptxt.get_width() // 2, r.centery - ptxt.get_height() // 2))

        pygame.draw.rect(screen, RED if back_btn.collidepoint(pygame.mouse.get_pos()) else (120, 40, 40), back_btn, border_radius=S(8))
        back_txt = font_s.render("< MENU", True, WHITE)
        screen.blit(back_txt, (back_btn.centerx - back_txt.get_width() // 2, back_btn.centery - back_txt.get_height() // 2))

        if pygame.time.get_ticks() - msg_time < 2000:
            m = font_m.render(msg_text, True, GOLD if "SUCCESS" in msg_text or "RECEIVED" in msg_text else RED)
            screen.blit(m, (W // 2 - m.get_width() // 2, H - S(40)))

        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                play_sfx("click")
                if back_btn.collidepoint(e.pos):
                    return
                if ad_btn.collidepoint(e.pos):
                    simulate_ad()
                    SAVE["gems"] += 10
                    write_save()
                    msg_text = "AD WATCHED! +10 GEMS RECEIVED 💎"
                    msg_time = pygame.time.get_ticks()
                for pkg in packages:
                    if pkg["rect"].collidepoint(e.pos):
                        if SAVE["gems"] >= pkg["gems"]:
                            SAVE["gems"] -= pkg["gems"]
                            BONUS += pkg["gold"]
                            write_save()
                            msg_text = f"SUCCESS! +${pkg['gold']} GOLD BONUS ADDED!"
                        else:
                            msg_text = "NOT ENOUGH GEMS!"
                        msg_time = pygame.time.get_ticks()
        clock.tick(60)
# ================= ================= =================
# 5. القائمة الرئيسية وواجهة الخريطة
# ================= ================= =================
def main_menu():
    bw, bh, gap = S(260), S(38), S(44)
    top = H // 2 - int(gap * 2.5)
    
    buttons = [
        {"txt": "MAP MODE", "desc": "Conquer 3 levels", "pos": [W // 2 - bw // 2, top, bw, bh], "mode": "MAP"},
        {"txt": "FREE PLAY", "desc": "Infinite respawn", "pos": [W // 2 - bw // 2, top + gap, bw, bh], "mode": "FREE"},
        {"txt": "BOSS MODE", "desc": "Balanced boss", "pos": [W // 2 - bw // 2, top + gap * 2, bw, bh], "mode": "BOSS"},
        {"txt": "GEM SHOP 💎", "desc": "Get gems & gold", "pos": [W // 2 - bw // 2, top + gap * 3, bw, bh], "mode": "SHOP"},
        {"txt": "HOW TO PLAY 📖", "desc": "Instructions", "pos": [W // 2 - bw // 2, top + gap * 4, bw, bh], "mode": "TUTORIAL"},
        {"txt": "SETTINGS ⚙️", "desc": "Audio & Sound", "pos": [W // 2 - bw // 2, top + gap * 5, bw, bh], "mode": "SETTINGS"},
        {"txt": "QUIT", "desc": "Exit Game", "pos": [W // 2 - bw // 2, top + gap * 6, bw, bh], "mode": "QUIT"},
    ]

    while True:
        draw_bg()
        pygame.draw.rect(screen, BLACK, (0, 0, W, S(55)))
        t = font_big.render("STICK WAR ULTRA", True, GOLD)
        screen.blit(t, (W // 2 - t.get_width() // 2, S(8)))
        
        for b in buttons:
            rect = pygame.Rect(b["pos"])
            col = GREEN if rect.collidepoint(pygame.mouse.get_pos()) else GRAY
            if b["mode"] == "QUIT":
                col = (120, 40, 40)
            elif b["mode"] == "SHOP":
                col = PURPLE if rect.collidepoint(pygame.mouse.get_pos()) else (100, 40, 140)
            elif b["mode"] == "TUTORIAL":
                col = BLUE if rect.collidepoint(pygame.mouse.get_pos()) else (40, 90, 140)
            elif b["mode"] == "SETTINGS":
                col = CYAN if rect.collidepoint(pygame.mouse.get_pos()) else (30, 100, 120)
                
            pygame.draw.rect(screen, col, rect, border_radius=S(10))
            txt = font_m.render(b["txt"], True, WHITE)
            screen.blit(txt, (rect.centerx - txt.get_width() // 2, rect.y + S(3)))
            d = font_s.render(b["desc"], True, WHITE)
            screen.blit(d, (rect.centerx - d.get_width() // 2, rect.y + S(21)))

        stats = font_s.render(f"Gems: {SAVE['gems']} 💎 | Streak: {SAVE['current_streak']} 🔥 | Zones: {SAVE['zones_conquered']}", True, CYAN)
        screen.blit(stats, (S(15), H - S(22)))
        
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                play_sfx("click")
                for b in buttons:
                    if pygame.Rect(b["pos"]).collidepoint(e.pos):
                        if b["mode"] == "QUIT":
                            pygame.quit()
                            sys.exit()
                        elif b["mode"] == "SHOP":
                            gems_shop()
                        elif b["mode"] == "TUTORIAL":
                            show_tutorial()
                        elif b["mode"] == "SETTINGS":
                            settings_screen()
                        else:
                            return b["mode"]
        clock.tick(60)

def show_map():
    play_sfx("click")
    owners = SAVE.get("map_owners", ["player", "enemy", "enemy"])
    MAP_NODES = [
        {"name": "MINE (1 ZONE)", "pos": [W * 0.3, H * 0.7], "towers": 2, "zones": 1, "reward": 50, "owner": owners[0]},
        {"name": "FOREST (2 ZONES)", "pos": [W * 0.6, H * 0.5], "towers": 3, "zones": 2, "reward": 50, "owner": owners[1]},
        {"name": "BOSS (3 ZONES)", "pos": [W * 0.5, H * 0.25], "towers": 3, "zones": 3, "reward": 50, "owner": owners[2]},
    ]
    CONN = [(0, 1), (1, 2)]
    back_btn = pygame.Rect(S(15), S(10), S(100), S(40))
    save_btn = pygame.Rect(W - S(140), S(10), S(125), S(40))

    saved_msg_time = 0

    while True:
        if all(n["owner"] == "player" for n in MAP_NODES):
            return "WIN"
        draw_bg()
        for a, b in CONN:
            pygame.draw.line(screen, (50, 50, 50), MAP_NODES[a]["pos"], MAP_NODES[b]["pos"], S(5))
        for node in MAP_NODES:
            col = GREEN if node["owner"] == "player" else RED
            pygame.draw.circle(screen, col, (int(node["pos"][0]), int(node["pos"][1])), S(40))
            txt = font_m.render(node["name"], True, WHITE)
            screen.blit(txt, (node["pos"][0] - txt.get_width() // 2, node["pos"][1] + S(55)))
            
        pygame.draw.rect(screen, BLACK, (0, 0, W, S(60)))
        t = font_b.render(f"MAP MODE | GEMS: {SAVE['gems']} 💎", True, CYAN)
        screen.blit(t, (W // 2 - t.get_width() // 2, S(15)))
        
        btn_col = RED if back_btn.collidepoint(pygame.mouse.get_pos()) else (120, 40, 40)
        pygame.draw.rect(screen, btn_col, back_btn, border_radius=S(8))
        btxt = font_s.render("< MENU", True, WHITE)
        screen.blit(btxt, (back_btn.centerx - btxt.get_width() // 2, back_btn.centery - btxt.get_height() // 2))

        scol = GREEN if save_btn.collidepoint(pygame.mouse.get_pos()) else (40, 120, 40)
        pygame.draw.rect(screen, scol, save_btn, border_radius=S(8))
        stxt = font_s.render("SAVE GAME 💾", True, WHITE)
        screen.blit(stxt, (save_btn.centerx - stxt.get_width() // 2, save_btn.centery - stxt.get_height() // 2))

        if pygame.time.get_ticks() - saved_msg_time < 1500:
            msg = font_m.render("GAME SAVED!", True, GOLD)
            screen.blit(msg, (W // 2 - msg.get_width() // 2, H - S(50)))

        pygame.display.flip()
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return "MENU"
            if e.type == pygame.MOUSEBUTTONDOWN:
                play_sfx("click")
                if back_btn.collidepoint(e.pos):
                    return "MENU"
                if save_btn.collidepoint(e.pos):
                    SAVE["map_owners"] = [n["owner"] for n in MAP_NODES]
                    write_save()
                    saved_msg_time = pygame.time.get_ticks()

                for idx, node in enumerate(MAP_NODES):
                    if math.hypot(e.pos[0] - node["pos"][0], e.pos[1] - node["pos"][1]) < S(45) and node["owner"] != "player":
                        res = battle(node, "MAP")
                   return "MENU"
                        if res:
                            node["owner"] = "player"
                            SAVE["zones_conquered"] += 1
                            SAVE["map_owners"] = [n["owner"] for n in MAP_NODES]
                            write_save()
        clock.tick(60)
# ================= ================= =================
# 6. منطق المعارك وتدفق اللعبة الأساسي (1)
# ================= ================= =================
def battle(node, game_mode="MAP"):
    global BONUS, SAVE
    play_sfx("click")
    is_boss = game_mode == "BOSS"
    is_free = game_mode == "FREE"
    uid_gen = itertools.count()

    if is_boss:
        castles = {
            "player": {"pos": [W // 2, int(H * 0.82)], "hp": 150, "money": 400 + BONUS, "income": 25, "color": GREEN, "max_hp": 150, "level": 1},
            "BOSS": {"pos": [W // 2, int(H * 0.18)], "hp": 500, "money": 200, "income": 30, "color": PURPLE, "max_hp": 500, "level": 1}
        }
        zones = [
            {"id": "LEFT", "pos": [W // 2 - S(200), H // 2], "r": S(75), "owner": "neutral", "cap": 0, "income": 20},
            {"id": "RIGHT", "pos": [W // 2 + S(200), H // 2], "r": S(75), "owner": "neutral", "cap": 0, "income": 20}
        ]
    elif is_free:
        castles = {
            "player": {"pos": [W // 2, int(H * 0.82)], "hp": 200, "money": 300 + BONUS, "income": 30, "color": GREEN, "max_hp": 200, "level": 1, "respawn": 0},
            "enemy1": {"pos": [W // 4, int(H * 0.15)], "hp": 150, "money": 150, "income": 20, "color": RED, "max_hp": 150, "level": 1, "respawn": 0},
            "enemy2": {"pos": [W * 3 // 4, int(H * 0.15)], "hp": 150, "money": 150, "income": 20, "color": BLUE, "max_hp": 150, "level": 1, "respawn": 0}
        }
        zones = [
            {"id": "MID", "pos": [W // 2, H // 2], "r": S(85), "owner": "neutral", "cap": 0, "income": 15},
            {"id": "LEFT", "pos": [W // 2 - S(200), H // 2], "r": S(70), "owner": "neutral", "cap": 0, "income": 12},
            {"id": "RIGHT", "pos": [W // 2 + S(200), H // 2], "r": S(70), "owner": "neutral", "cap": 0, "income": 12}
        ]
    else:
        castles = {
            "player": {"pos": [W // 2, int(H * 0.82)], "hp": 120, "money": 250 + BONUS, "income": 20, "color": GREEN, "max_hp": 120},
            "enemy1": {"pos": [W // 4, int(H * 0.15)], "hp": 120, "money": 120, "income": 20, "color": RED, "max_hp": 120}
        }
        if node.get("towers", 0) >= 3:
            castles["enemy2"] = {"pos": [W * 3 // 4, int(H * 0.15)], "hp": 120, "money": 120, "income": 20, "color": BLUE, "max_hp": 120}
        if node.get("zones", 1) == 1:
            zones = [{"id": "MID", "pos": [W // 2, H // 2], "r": S(85), "owner": "neutral", "cap": 0, "income": 15}]
        elif node.get("zones", 1) == 2:
            zones = [
                {"id": "LEFT", "pos": [W // 2 - S(190), H // 2], "r": S(70), "owner": "neutral", "cap": 0, "income": 12},
                {"id": "RIGHT", "pos": [W // 2 + S(190), H // 2], "r": S(70), "owner": "neutral", "cap": 0, "income": 12}
            ]
        else:
            zones = [
                {"id": "MID", "pos": [W // 2, H // 2], "r": S(80), "owner": "neutral", "cap": 0, "income": 12},
                {"id": "LEFT", "pos": [W // 2 - S(210), H // 2], "r": S(65), "owner": "neutral", "cap": 0, "income": 10},
                {"id": "RIGHT", "pos": [W // 2 + S(210), H // 2], "r": S(65), "owner": "neutral", "cap": 0, "income": 10}
            ]

    soldiers = []
    crates = []
    mode = "MID"
    selected = "WARRIOR"
    shake = 0
    paused = False

    def build_rects():
        rects = {}
        x = S(5)
        for name in ["DEFEND"] + [z["id"] for z in zones] + [n for n in castles if n != "player"]:
            rects[name] = pygame.Rect(x, H - S(65), S(70), S(55))
            x += S(75)
        return rects

    control_rects = build_rects()
    
    shop_rects = {}
    sy = H // 2 - S(160)
    for tk in TROOP_KEYS:
        shop_rects[tk] = pygame.Rect(W - S(105), sy, S(95), S(45))
        sy += S(52)

    pause_btn = pygame.Rect(W - S(60), S(10), S(50), S(50))
    resume_btn = pygame.Rect(W // 2 - S(110), H // 2 - S(20), S(220), S(60))
    quit_btn = pygame.Rect(W // 2 - S(110), H // 2 + S(55), S(220), S(60))

    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
    pygame.time.set_timer(pygame.USEREVENT + 2, 8000)
    while True:
        draw_bg(shake)
        if shake > 0:
            shake -= 1

        if is_free:
            for c_name, c_data in castles.items():
                if c_name != "player" and c_data["hp"] <= 0:
                    if c_data.get("respawn", 0) <= 0:
                        c_data["respawn"] = 300
                    else:
                        c_data["respawn"] -= 1
                        if c_data["respawn"] == 0:
                            c_data["hp"] = c_data["max_hp"]
                            c_data["money"] = 150

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "MENU"
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_sfx("click")
                mx, my = event.pos
                if pause_btn.collidepoint(mx, my):
                    paused = not paused
                elif paused:
                    if resume_btn.collidepoint(mx, my):
                        paused = False
                    elif quit_btn.collidepoint(mx, my):
                        return "MENU"
                else:
                    for cr in crates[:]:
                        if math.hypot(mx - cr["pos"][0], my - cr["pos"][1]) < S(45):
                            castles["player"]["money"] += cr["money"]
                            crates.remove(cr)
                    
                    for name, rect in shop_rects.items():
                        if rect.collidepoint(mx, my):
                            selected = name
                            break
                    else:
                        p_pos = castles["player"]["pos"]
                        if math.hypot(mx - p_pos[0], my - p_pos[1]) < S(45):
                            mode = "DEFEND"
                        else:
                            attacked_castle = False
                            for c_name, c_data in castles.items():
                                if c_name != "player" and c_data["hp"] > 0:
                                    rad = S(40) if is_boss and c_name == "BOSS" else S(28)
                                    if math.hypot(mx - c_data["pos"][0], my - c_data["pos"][1]) < rad + S(20):
                                        mode = c_name
                                        attacked_castle = True
                                        break
                            
                            if not attacked_castle:
                                for z in zones:
                                    if math.hypot(mx - z["pos"][0], my - z["pos"][1]) < z["r"]:
                                        mode = z["id"]
                                        break
                                else:
                                    for name, rect in control_rects.items():
                                        if rect.collidepoint(mx, my):
                                            mode = name
                                            break
                        
                        if castles["player"]["money"] >= TROOPS[selected]["cost"]:
                            castles["player"]["money"] -= TROOPS[selected]["cost"]
                            play_sfx("spawn")
                            uid = next(uid_gen)
                            if mode == "DEFEND":
                                hx = castles["player"]["pos"][0] + random.randint(-S(120), S(120))
                                hy = castles["player"]["pos"][1] - S(100)
                                soldiers.append({"uid": uid, "pos": list(castles["player"]["pos"]), "team": "player", "type": selected, "job": "DEFEND_BASE", "home": [hx, hy], "hp": TROOPS[selected]["hp"], "acd": 0})
                            elif mode in [z["id"] for z in zones]:
                                tz = next((z for z in zones if z["id"] == mode), zones[0])
                                soldiers.append({"uid": uid, "pos": list(castles["player"]["pos"]), "team": "player", "type": selected, "job": "GUARD_ZONE", "zone_id": tz["id"], "home": list(tz["pos"]), "hp": TROOPS[selected]["hp"], "acd": 0})
                            elif mode in castles:
                                soldiers.append({"uid": uid, "pos": list(castles["player"]["pos"]), "team": "player", "type": selected, "job": "ATTACK", "target": mode, "hp": TROOPS[selected]["hp"], "acd": 0})

            if event.type == pygame.USEREVENT + 1 and not paused:
                for c in castles.values():
                    if c["hp"] > 0:
                        c["money"] += c["income"]
                for z in zones:
                    if z["owner"] in castles and castles[z["owner"]]["hp"] > 0:
                        castles[z["owner"]]["money"] += z["income"]

            if event.type == pygame.USEREVENT + 2 and not paused and len(crates) < 3:
                crates.append({"pos": [random.randint(W // 4, W * 3 // 4), random.randint(H // 3, H * 2 // 3)], "money": 100})
        if paused:
            pygame.draw.rect(screen, BLACK, (W // 2 - S(130), H // 2 - S(80), S(260), S(220)), border_radius=S(15))
            pygame.draw.rect(screen, GREEN, resume_btn, border_radius=S(10))
            pygame.draw.rect(screen, RED, quit_btn, border_radius=S(10))
            rt = font_m.render("RESUME", True, WHITE)
            screen.blit(rt, (resume_btn.centerx - rt.get_width() // 2, resume_btn.centery - rt.get_height() // 2))
            qt = font_m.render("QUIT TO MENU", True, WHITE)
            screen.blit(qt, (quit_btn.centerx - qt.get_width() // 2, quit_btn.centery - qt.get_height() // 2))
            pygame.display.flip()
            clock.tick(60)
            continue

        if castles["player"]["money"] > SAVE["best_free_money"]:
            SAVE["best_free_money"] = castles["player"]["money"]
            write_save()

        for en in [n for n in castles if n != "player"]:
            if castles[en]["hp"] <= 0 or castles[en]["money"] < 20:
                continue
            if random.random() > 0.05:
                continue
            etype = random.choice(TROOP_KEYS) if castles[en]["money"] >= 20 else "WARRIOR"
            if castles[en]["money"] < TROOPS[etype]["cost"]:
                continue
            castles[en]["money"] -= TROOPS[etype]["cost"]
            uid = next(uid_gen)
            if is_boss:
                if random.random() < 0.5:
                    tz = random.choice(zones)
                    soldiers.append({"uid": uid, "pos": list(castles[en]["pos"]), "team": en, "type": etype, "job": "GUARD_ZONE", "zone_id": tz["id"], "home": list(tz["pos"]), "hp": TROOPS[etype]["hp"], "acd": 0})
                else:
                    soldiers.append({"uid": uid, "pos": list(castles[en]["pos"]), "team": en, "type": etype, "job": "ATTACK", "target": "player", "hp": TROOPS[etype]["hp"], "acd": 0})
            else:
                choice = random.choice(["DEFEND"] + [z["id"] for z in zones] + ["player"])
                if choice == "DEFEND":
                    hx = castles[en]["pos"][0] + random.randint(-100, 100)
                    hy = castles[en]["pos"][1] + 100
                    soldiers.append({"uid": uid, "pos": list(castles[en]["pos"]), "team": en, "type": etype, "job": "DEFEND_BASE", "home": [hx, hy], "hp": TROOPS[etype]["hp"], "acd": 0})
                elif choice in [z["id"] for z in zones]:
                    tz = next((z for z in zones if z["id"] == choice), None)
                    if tz:
                        soldiers.append({"uid": uid, "pos": list(castles[en]["pos"]), "team": en, "type": etype, "job": "GUARD_ZONE", "zone_id": tz["id"], "home": list(tz["pos"]), "hp": TROOPS[etype]["hp"], "acd": 0})
                else:
                    soldiers.append({"uid": uid, "pos": list(castles[en]["pos"]), "team": en, "type": etype, "job": "ATTACK", "target": "player", "hp": TROOPS[etype]["hp"], "acd": 0})

        to_del = set()
        for s in soldiers:
            if s["job"] == "ATTACK" and (s["target"] not in castles or castles[s["target"]]["hp"] <= 0):
                to_del.add(s["uid"])
                continue
            
            if s["job"] == "DEFEND_BASE":
                my_castle = castles[s["team"]]["pos"]
                enemies_near_base = [
                    e for e in soldiers 
                    if e["team"] != s["team"] and e["uid"] not in to_del 
                    and math.hypot(e["pos"][0] - my_castle[0], e["pos"][1] - my_castle[1]) < S(250)
                ]
                if enemies_near_base:
                    nearest_enemy = min(enemies_near_base, key=lambda e: math.hypot(s["pos"][0] - e["pos"][0], s["pos"][1] - e["pos"][1]))
                    dest = nearest_enemy["pos"]
                else:
                    dest = s["home"]
            elif s["job"] == "GUARD_ZONE":
                mz = next((z for z in zones if z["id"] == s["zone_id"]), zones[0])
                ens = [e for e in soldiers if e["team"] != s["team"] and e["uid"] not in to_del and math.hypot(e["pos"][0] - mz["pos"][0], e["pos"][1] - mz["pos"][1]) < mz["r"] + 20]
                ne = min(ens, key=lambda e: math.hypot(s["pos"][0] - e["pos"][0], s["pos"][1] - e["pos"][1]), default=None)
                dest = ne["pos"] if ne else s["home"]
            else:
                dest = castles[s["target"]]["pos"]
            
            dx = dest[0] - s["pos"][0]
            dy = dest[1] - s["pos"][1]
            d = math.hypot(dx, dy)
            if d > 5:
                s["pos"][0] += (dx / d) * TROOPS[s["type"]]["speed"]
                s["pos"][1] += (dy / d) * TROOPS[s["type"]]["speed"]
            else:
                if s["job"] == "ATTACK":
                    s["acd"] = s.get("acd", 0) - 1
                    if s["acd"] <= 0:
                        castles[s["target"]]["hp"] -= TROOPS[s["type"]]["dmg"]
                        play_sfx("hit")
                        if s["target"] == "player":
                            shake = 8
                        
                        if is_free and castles[s["target"]]["hp"] <= 0:
                            SAVE["gems"] += 10
                            write_save()

                        if TROOPS[s["type"]].get("ranged"):
                            s["acd"] = TROOPS[s["type"]].get("cd", 40)
                        else:
                            to_del.add(s["uid"])
        for i in range(len(soldiers)):
            for j in range(i + 1, len(soldiers)):
                s1 = soldiers[i]
                s2 = soldiers[j]
                if s1["uid"] in to_del or s2["uid"] in to_del or s1["team"] == s2["team"]:
                    continue
                if math.hypot(s1["pos"][0] - s2["pos"][0], s1["pos"][1] - s2["pos"][1]) < 16:
                    s1["hp"] -= 1
                    s2["hp"] -= 1
                    play_sfx("hit")
                    if s1["hp"] <= 0:
                        to_del.add(s1["uid"])
                    if s2["hp"] <= 0:
                        to_del.add(s2["uid"])
        soldiers = [s for s in soldiers if s["uid"] not in to_del]

        for z in zones:
            cnt = {}
            for s in soldiers:
                if s["job"] == "GUARD_ZONE" and s["zone_id"] == z["id"]:
                    if math.hypot(s["pos"][0] - z["pos"][0], s["pos"][1] - z["pos"][1]) < z["r"]:
                        cnt[s["team"]] = cnt.get(s["team"], 0) + 1
            if cnt and len(cnt) == 1:
                best = list(cnt.keys())[0]
                if z["owner"] != best:
                    z["cap"] += 1
                    if z["cap"] >= 80:
                        z["owner"] = best
                        z["cap"] = 0

        for z in zones:
            col = NEUTRAL if z["owner"] == "neutral" else castles[z["owner"]]["color"] if z["owner"] in castles else NEUTRAL
            pygame.draw.circle(screen, col, (int(z["pos"][0]), int(z["pos"][1])), z["r"])
            pygame.draw.circle(screen, BLACK, (int(z["pos"][0]), int(z["pos"][1])), z["r"], S(4))
            if z["cap"] > 0:
                pygame.draw.rect(screen, WHITE, (z["pos"][0] - z["r"], z["pos"][1] - z["r"] - S(12), int(z["cap"] / 80 * z["r"] * 2), S(7)))
            screen.blit(font_s.render(f"{z['id']}", True, BLACK), (z["pos"][0] - S(15), z["pos"][1] - S(10)))

        for cr in crates:
            pygame.draw.rect(screen, GOLD, (cr["pos"][0] - S(15), cr["pos"][1] - S(15), S(30), S(30)), border_radius=S(5))

        for name, c in castles.items():
            rad = S(40) if is_boss and name == "BOSS" else S(28)
            if c["hp"] <= 0:
                if is_free and name != "player":
                    rem_sec = max(1, int(c.get("respawn", 0) / 60) + 1)
                    rtxt = font_s.render(f"RESPAWN: {rem_sec}s", True, GOLD)
                    screen.blit(rtxt, (c["pos"][0] - rtxt.get_width() // 2, c["pos"][1] - S(10)))
                continue

            pygame.draw.circle(screen, c["color"], (int(c["pos"][0]), int(c["pos"][1])), rad)
            bar = int(max(0, c["hp"]) / c["max_hp"] * S(56))
            pygame.draw.rect(screen, (100, 0, 0), (c["pos"][0] - S(28), c["pos"][1] - S(38), S(56), S(8)))
            pygame.draw.rect(screen, GREEN, (c["pos"][0] - S(28), c["pos"][1] - S(38), bar, S(8)))

        for s in soldiers:
            col = castles[s["team"]]["color"] if s["team"] in castles else RED
            pygame.draw.circle(screen, col, (int(s["pos"][0]), int(s["pos"][1])), TROOPS[s["type"]]["r"] + 2)

        screen.blit(font_m.render(f"${castles['player']['money']} MODE:{mode}", True, GOLD), (S(15), S(20)))

        for name, rect in control_rects.items():
            col = GREEN if mode == name else GRAY
            pygame.draw.rect(screen, col, rect, border_radius=S(8))
            screen.blit(font_s.render(name, True, WHITE), (rect.centerx - S(20), rect.centery - S(8)))
            
        for name, rect in shop_rects.items():
            col = GREEN if selected == name else (40, 40, 40)
            pygame.draw.rect(screen, col, rect, border_radius=S(8))
            txt_name = font_s.render(name, True, WHITE)
            txt_cost = font_s.render(f"${TROOPS[name]['cost']}", True, GOLD)
            screen.blit(txt_name, (rect.x + S(4), rect.y + S(4)))
            screen.blit(txt_cost, (rect.x + S(4), rect.y + S(22)))

        pygame.draw.rect(screen, (40, 40, 40), pause_btn, border_radius=S(8))
        pt = font_s.render("II", True, WHITE)
        screen.blit(pt, (pause_btn.centerx - pt.get_width() // 2, pause_btn.centery - pt.get_height() // 2))

        if castles["player"]["hp"] <= 0:
            SAVE["current_streak"] = 0
            write_save()
            result_screen("DEFEAT!", "Game Over", RED)
            return False
            
        enemies_alive = [n for n, c in castles.items() if n != "player" and c["hp"] > 0]
        if not enemies_alive and not is_free:
            SAVE["current_streak"] += 1
            if SAVE["current_streak"] > SAVE["best_streak"]:
                SAVE["best_streak"] = SAVE["current_streak"]
            
            base_reward = 200 if is_boss else 50
            
            streak_bonus = 0
            if SAVE["current_streak"] >= 5:
                streak_bonus = 15
            elif SAVE["current_streak"] >= 3:
                streak_bonus = 5
                
            total_gems = base_reward + streak_bonus
            SAVE["gems"] += total_gems
            write_save()
            
            sub_msg = f"+{base_reward} GEMS REWARDED! 💎"
       
