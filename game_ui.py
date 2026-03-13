"""
game_ui.py  –  pygame display layer for Hitchhiker's Tic-Tac-Toe
Run game_play.py to start the game.
"""

import os
import random
import sys

import pygame

# ─────────────────────────────────────────────────────────────────────────────
#  INITIALISE
# ─────────────────────────────────────────────────────────────────────────────

pygame.init()

W, H   = 1280, 720
screen = pygame.display.set_mode((W, H))
clock  = pygame.time.Clock()

# ─────────────────────────────────────────────────────────────────────────────
#  FONTS
# ─────────────────────────────────────────────────────────────────────────────

_FONT_FILE = "Harlow Solid Regular.ttf"

def _font(size):
    try:
        return pygame.font.Font(_FONT_FILE, size)
    except FileNotFoundError:
        return pygame.font.SysFont("serif", size)

F_TITLE   = _font(90)
F_OVERLAY = _font(60)
F_INPUT   = _font(40)
F_LABEL   = _font(34)
F_SCORE   = _font(34)
F_QUOTE   = _font(26)
F_BUTTON  = _font(36)

# ─────────────────────────────────────────────────────────────────────────────
#  WINDOW CAPTION
# ─────────────────────────────────────────────────────────────────────────────

_CAPTIONS = [
    "Hitchhiker's Tic-Tac-Toe",
    "Brain the size of a planet, and I'm a window title.",
    "Don't panic. Or do. I don't care.",
    "42: The answer to how to win.",
    "Life, loathe it or ignore it, you can't like it.",
    "Everything is quite remarkably pointless.",
]
pygame.display.set_caption(random.choice(_CAPTIONS))

# ─────────────────────────────────────────────────────────────────────────────
#  COLOURS
# ─────────────────────────────────────────────────────────────────────────────

C_DARK        = ( 20,  20,  20)
C_WHITE       = (255, 255, 255)
C_YELLOW      = (255, 220,  50)
C_GREY        = ( 60,  60,  60)
C_RED         = (180,  30,  30)
C_RED_HOV     = (220,  50,  50)
C_GREEN       = ( 40, 130,  40)
C_GREEN_HOV   = ( 60, 180,  60)
C_BLUE        = ( 40, 110, 200)
C_BLUE_HOV    = ( 60, 150, 240)
C_INPUT_IDLE  = (220, 220, 220)
C_INPUT_ACT   = (255, 255, 200)
C_PLACEHOLDER = (140, 140, 140)

# ─────────────────────────────────────────────────────────────────────────────
#  BACKGROUND IMAGES
# ─────────────────────────────────────────────────────────────────────────────

_BG_FILES = [
    "babel-fish.png",
    "hitchikers.png",
    "arthur_dent.png",
    "restaurant.png",
]

def _load_bg(path):
    img = pygame.image.load(path).convert()
    return pygame.transform.scale(img, (W, H))

_bg = _load_bg(random.choice(_BG_FILES))

def randomize_background():
    global _bg
    _bg = _load_bg(random.choice(_BG_FILES))

# ─────────────────────────────────────────────────────────────────────────────
#  GAME PIECE ICONS
# ─────────────────────────────────────────────────────────────────────────────

_ICON_SIZE = (160, 160)
_ICON_X    = pygame.transform.scale(
                 pygame.image.load("vorgon.png").convert_alpha(), _ICON_SIZE)
_ICON_O    = pygame.transform.scale(
                 pygame.image.load("dont_panic.png").convert_alpha(), _ICON_SIZE)

SYM_X = "X"
SYM_O = "O"

# ─────────────────────────────────────────────────────────────────────────────
#  MENU ASSETS
# ─────────────────────────────────────────────────────────────────────────────

try:
    _MARVIN_IMG = pygame.transform.scale(
        pygame.image.load("marvin.png").convert_alpha(), (180, 180))
except Exception:
    _MARVIN_IMG = None

try:
    _TITLE_IMG = pygame.transform.scale(
        pygame.image.load("hitchikers.png").convert_alpha(), (560, 150))
except Exception:
    _TITLE_IMG = None

# ─────────────────────────────────────────────────────────────────────────────
#  GAMEPLAY RECTS
# ─────────────────────────────────────────────────────────────────────────────

_RESET_RECT      = pygame.Rect(W - 310,        H - 70,        290, 55)
_PLAY_AGAIN_RECT = pygame.Rect(W // 2 - 195,   H // 2 + 70,   175, 55)
_QUIT_RECT       = pygame.Rect(W // 2 +  20,   H // 2 + 70,   175, 55)

# ─────────────────────────────────────────────────────────────────────────────
#  SHARED HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _wrap(text, fnt, max_w):
    words, lines, cur = text.split(), [], []
    for w in words:
        test = " ".join(cur + [w])
        if fnt.size(test)[0] <= max_w:
            cur.append(w)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [w]
    if cur:
        lines.append(" ".join(cur))
    return lines

def _btn(rect, label, fnt, bg, fg=C_WHITE, border=C_WHITE):
    pygame.draw.rect(screen, bg,     rect, border_radius=8)
    pygame.draw.rect(screen, border, rect, 2, border_radius=8)
    s = fnt.render(label, True, fg)
    screen.blit(s, s.get_rect(center=rect.center))

def _panel(x, y, w, h, alpha=180):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    surf.fill((0, 0, 0, alpha))
    screen.blit(surf, (x, y))

# ─────────────────────────────────────────────────────────────────────────────
#  GAMEPLAY FRAME
# ─────────────────────────────────────────────────────────────────────────────

def draw_game_window(board, p1_name, p1_score, p2_name, p2_score, draws,
                     marvin_quote=""):
    screen.blit(_bg, (0, 0))

    # Grid
    for gx in (W // 3, 2 * W // 3):
        pygame.draw.line(screen, C_WHITE, (gx, 0), (gx, H), 4)
    for gy in (H // 3, 2 * H // 3):
        pygame.draw.line(screen, C_WHITE, (0, gy), (W, gy), 4)

    # Pieces
    cw, ch = W // 3, H // 3
    for i, cell in enumerate(board):
        if cell in (SYM_X, SYM_O):
            row, col = divmod(i, 3)
            cx = col * cw + cw // 2 - _ICON_SIZE[0] // 2
            cy = row * ch + ch // 2 - _ICON_SIZE[1] // 2
            screen.blit(_ICON_X if cell == SYM_X else _ICON_O, (cx, cy))

    # Abandon Hope button
    mx, my = pygame.mouse.get_pos()
    _btn(_RESET_RECT, "Abandon Hope", F_BUTTON,
         bg=C_RED_HOV if _RESET_RECT.collidepoint(mx, my) else C_RED)

    # Score strip
    sc = f"{p1_name}: {p1_score}   {p2_name}: {p2_score}   Draws: {draws}"
    screen.blit(F_SCORE.render(sc, True, C_DARK),   (22, H - 50))
    screen.blit(F_SCORE.render(sc, True, C_YELLOW), (20, H - 52))

    # Marvin quote banner
    if marvin_quote:
        lines = _wrap(marvin_quote, F_QUOTE, W - 40)
        bh = len(lines) * 34 + 14
        _panel(0, 0, W, bh, 190)
        for j, line in enumerate(lines):
            s = F_QUOTE.render(line, True, C_YELLOW)
            screen.blit(s, s.get_rect(centerx=W // 2, y=7 + j * 34))

    pygame.display.flip()

# ─────────────────────────────────────────────────────────────────────────────
#  RESULT OVERLAY
# ─────────────────────────────────────────────────────────────────────────────

def show_result_overlay(board, headline, subtext,
                        p1_name, p1_score, p2_name, p2_score, draws):
    """Blocking result screen. Returns True = play again, False = quit."""
    pygame.event.clear()

    # ── Build a static background surface once ────────────────────────────────
    # Render the board + panel + headline + subtext into a surface so the
    # per-frame loop never has to re-render text (eliminates flicker).
    pw, ph = 780, 300
    panel_x = (W - pw) // 2
    panel_y = H // 2 - 160

    static = pygame.Surface((W, H))
    draw_game_window(board, p1_name, p1_score, p2_name, p2_score, draws)
    static.blit(screen, (0, 0))          # capture board state

    overlay = pygame.Surface((pw, ph), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 210))
    static.blit(overlay, (panel_x, panel_y))

    h_s = F_OVERLAY.render(headline, True, C_YELLOW)
    static.blit(h_s, h_s.get_rect(centerx=W // 2, y=panel_y + 15))

    lines = _wrap(subtext, F_QUOTE, pw - 40)
    for j, line in enumerate(lines):
        s = F_QUOTE.render(line, True, C_WHITE)
        static.blit(s, s.get_rect(centerx=W // 2, y=panel_y + 80 + j * 32))

    # ── Hover state tracking ──────────────────────────────────────────────────
    prev_hover = (False, False)   # (play_again_hovered, quit_hovered)

    def _draw_buttons(pa_hov, q_hov):
        screen.blit(static, (0, 0))
        _btn(_PLAY_AGAIN_RECT, "Play Again", F_BUTTON,
             bg=C_GREEN_HOV if pa_hov else C_GREEN)
        _btn(_QUIT_RECT, "Quit", F_BUTTON,
             bg=C_RED_HOV if q_hov else C_RED)
        pygame.display.flip()

    # Initial draw
    mx, my = pygame.mouse.get_pos()
    cur_hover = (_PLAY_AGAIN_RECT.collidepoint(mx, my),
                 _QUIT_RECT.collidepoint(mx, my))
    _draw_buttons(*cur_hover)
    prev_hover = cur_hover

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.MOUSEMOTION:
                cur_hover = (_PLAY_AGAIN_RECT.collidepoint(ev.pos),
                             _QUIT_RECT.collidepoint(ev.pos))
                if cur_hover != prev_hover:
                    _draw_buttons(*cur_hover)
                    prev_hover = cur_hover

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                if _PLAY_AGAIN_RECT.collidepoint(ev.pos):
                    return True
                if _QUIT_RECT.collidepoint(ev.pos):
                    return False

        clock.tick(60)

# ─────────────────────────────────────────────────────────────────────────────
#  TIMED MESSAGE BANNER
# ─────────────────────────────────────────────────────────────────────────────

def show_message(text, board, p1_name, p1_score, p2_name, p2_score, draws,
                 duration_ms=2500):
    """Show a centred message banner for duration_ms ms, then return."""
    pygame.event.clear()
    lines    = _wrap(text, F_QUOTE, W - 80)
    bh       = len(lines) * 34 + 24
    deadline = pygame.time.get_ticks() + duration_ms

    # Draw once
    draw_game_window(board, p1_name, p1_score, p2_name, p2_score, draws)
    _panel((W - 900) // 2, H // 2 - bh // 2 - 10, 900, bh + 20, 200)
    for j, line in enumerate(lines):
        s = F_QUOTE.render(line, True, C_YELLOW)
        screen.blit(s, s.get_rect(centerx=W // 2, y=H // 2 - bh // 2 + j * 34))
    pygame.display.flip()

    # Just wait out the timer, draining quit events only
    while pygame.time.get_ticks() < deadline:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        clock.tick(30)

# ─────────────────────────────────────────────────────────────────────────────
#  MENU  (event-driven – only redraws on change, never flickers)
# ─────────────────────────────────────────────────────────────────────────────

def ui_menu(returning=False):
    """
    Setup menu. Returns (p1_name, p2_name, mode, order).
    mode  "1" = human vs human   "2" = human vs Marvin
    order "1" = P1 first         "2" = P2 / Marvin first
    """
    # ── layout ───────────────────────────────────────────────────────────────
    LBL_X   = 150
    FLD_X   = 420
    FLD_W   = 400
    FLD_H   = 50
    BTN_W   = 190
    BTN_H   = 52
    BTN_GAP = 24
    ROW0_Y  = 205
    ROW_GAP = 98

    row_y = [ROW0_Y + i * ROW_GAP for i in range(5)]

    p1_rect    = pygame.Rect(FLD_X,                    row_y[0], FLD_W,   FLD_H)
    mh_rect    = pygame.Rect(FLD_X,                    row_y[1], BTN_W,   BTN_H)
    mm_rect    = pygame.Rect(FLD_X + BTN_W + BTN_GAP, row_y[1], BTN_W,   BTN_H)
    p2_rect    = pygame.Rect(FLD_X,                    row_y[2], FLD_W,   FLD_H)
    of_rect    = pygame.Rect(FLD_X,                    row_y[3], BTN_W,   BTN_H)
    os_rect    = pygame.Rect(FLD_X + BTN_W + BTN_GAP, row_y[3], BTN_W,   BTN_H)
    start_rect = pygame.Rect(W // 2 - 150,             row_y[4], 300,     60)

    # ── state ────────────────────────────────────────────────────────────────
    p1_text   = ""
    p2_text   = ""
    mode      = "2"
    order     = "1"
    focus     = "p1"
    error_msg = ""
    cursor_on = True

    # Cursor blink via a pygame USEREVENT timer (fires every 500 ms)
    CURSOR_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(CURSOR_EVENT, 500)

    # ── draw helpers ─────────────────────────────────────────────────────────
    def _label(text, y):
        s = F_LABEL.render(text, True, C_YELLOW)
        screen.blit(s, (LBL_X, y + (FLD_H - s.get_height()) // 2))

    def _input_box(rect, text, active, placeholder=""):
        bg  = C_INPUT_ACT  if active else C_INPUT_IDLE
        bdr = C_YELLOW     if active else C_WHITE
        pygame.draw.rect(screen, bg,  rect, border_radius=8)
        pygame.draw.rect(screen, bdr, rect, 2, border_radius=8)
        if text:
            display = text + ("|" if (active and cursor_on) else " ")
            s = F_INPUT.render(display, True, C_DARK)
        else:
            if active and cursor_on:
                s = F_INPUT.render("|", True, C_DARK)
            else:
                s = F_INPUT.render(placeholder, True, C_PLACEHOLDER)
        screen.blit(s, s.get_rect(midleft=(rect.x + 12, rect.centery)))

    def _toggle(rect, label, selected, hovered):
        bg = C_BLUE if selected else (C_BLUE_HOV if hovered else C_GREY)
        pygame.draw.rect(screen, bg,      rect, border_radius=8)
        pygame.draw.rect(screen, C_WHITE, rect, 2,            border_radius=8)
        s = F_BUTTON.render(label, True, C_WHITE)
        screen.blit(s, s.get_rect(center=rect.center))

    def _draw_menu(mx, my):
        """Render the complete menu frame."""
        screen.blit(_bg, (0, 0))
        _panel(60, 20, W - 120, H - 40, 175)

        if _TITLE_IMG:
            screen.blit(_TITLE_IMG, (W // 2 - _TITLE_IMG.get_width() // 2, 30))
        else:
            ts = F_TITLE.render("Hitchhiker's Tic-Tac-Toe", True, C_YELLOW)
            screen.blit(ts, ts.get_rect(centerx=W // 2, y=30))

        sub = ("Welcome back to the end of the universe" if returning
               else "Don't Panic — fill in your details and press Start")
        ss = F_QUOTE.render(sub, True, C_WHITE)
        screen.blit(ss, ss.get_rect(centerx=W // 2, y=175))

        _label("Player 1:",    row_y[0])
        _input_box(p1_rect, p1_text, focus == "p1", "Enter name…")

        _label("Play against:", row_y[1])
        _toggle(mh_rect, "Human",     mode == "1", mh_rect.collidepoint(mx, my))
        _toggle(mm_rect, "Marvin 🤖", mode == "2", mm_rect.collidepoint(mx, my))

        if mode == "1":
            _label("Player 2:", row_y[2])
            _input_box(p2_rect, p2_text, focus == "p2", "Enter name…")
        else:
            if _MARVIN_IMG:
                screen.blit(_MARVIN_IMG, (FLD_X, row_y[2] - 15))
                ms = F_LABEL.render("Marvin the Paranoid Android", True, (180, 180, 255))
                screen.blit(ms, (FLD_X + _MARVIN_IMG.get_width() + 16,
                                 row_y[2] + (FLD_H - ms.get_height()) // 2))
            else:
                ms = F_LABEL.render("Marvin the Paranoid Android", True, (180, 180, 255))
                screen.blit(ms, (FLD_X, row_y[2] + (FLD_H - ms.get_height()) // 2))

        _label("You go:", row_y[3])
        _toggle(of_rect, "First  ❌",  order == "1", of_rect.collidepoint(mx, my))
        _toggle(os_rect, "Second ⭕", order == "2", os_rect.collidepoint(mx, my))

        s_hov = start_rect.collidepoint(mx, my)
        pygame.draw.rect(screen, C_GREEN_HOV if s_hov else C_GREEN,
                         start_rect, border_radius=10)
        pygame.draw.rect(screen, C_YELLOW, start_rect, 2, border_radius=10)
        st = F_OVERLAY.render("Start Game", True, C_YELLOW)
        screen.blit(st, st.get_rect(center=start_rect.center))

        if error_msg:
            es = F_QUOTE.render(error_msg, True, (255, 80, 80))
            screen.blit(es, es.get_rect(centerx=W // 2, y=start_rect.bottom + 12))

        pygame.display.flip()

    # Initial draw
    _draw_menu(*pygame.mouse.get_pos())

    # ── event loop ────────────────────────────────────────────────────────────
    while True:
        needs_redraw = False

        for ev in pygame.event.get():

            if ev.type == pygame.QUIT:
                pygame.time.set_timer(CURSOR_EVENT, 0)
                pygame.quit(); sys.exit()

            # Cursor blink (timer event)
            elif ev.type == CURSOR_EVENT:
                cursor_on    = not cursor_on
                needs_redraw = True

            # Mouse moved → may change button hover colour
            elif ev.type == pygame.MOUSEMOTION:
                needs_redraw = True

            elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                pos = ev.pos
                needs_redraw = True

                if p1_rect.collidepoint(pos):
                    focus = "p1"; cursor_on = True

                elif mode == "1" and p2_rect.collidepoint(pos):
                    focus = "p2"; cursor_on = True

                elif mh_rect.collidepoint(pos):
                    mode = "1"; focus = "p2"; cursor_on = True

                elif mm_rect.collidepoint(pos):
                    mode = "2"; p2_text = ""; focus = "p1"; cursor_on = True

                elif of_rect.collidepoint(pos):
                    order = "1"

                elif os_rect.collidepoint(pos):
                    order = "2"

                elif start_rect.collidepoint(pos):
                    if not p1_text.strip():
                        error_msg = "Player 1 needs a name — the universe won't wait forever."
                    elif mode == "1" and not p2_text.strip():
                        error_msg = "Player 2 needs a name too, or switch to Marvin."
                    else:
                        pygame.time.set_timer(CURSOR_EVENT, 0)  # stop timer
                        pygame.event.clear()
                        p2 = p2_text.strip() if mode == "1" else "Marvin 🤖"
                        return p1_text.strip(), p2, mode, order

            elif ev.type == pygame.KEYDOWN:
                error_msg    = ""
                needs_redraw = True

                if ev.key == pygame.K_ESCAPE:
                    pygame.time.set_timer(CURSOR_EVENT, 0)
                    pygame.quit(); sys.exit()

                elif ev.key == pygame.K_TAB:
                    if mode == "1":
                        focus = "p2" if focus == "p1" else "p1"
                    cursor_on = True

                elif ev.key == pygame.K_RETURN:
                    if focus == "p1" and mode == "1" and p1_text.strip():
                        focus = "p2"; cursor_on = True
                    elif p1_text.strip() and (mode == "2" or p2_text.strip()):
                        pygame.time.set_timer(CURSOR_EVENT, 0)
                        pygame.event.clear()
                        p2 = p2_text.strip() if mode == "1" else "Marvin 🤖"
                        return p1_text.strip(), p2, mode, order
                    else:
                        error_msg = "Player 1 needs a name — the universe won't wait forever."

                elif ev.key == pygame.K_BACKSPACE:
                    if focus == "p1" and p1_text:
                        p1_text = p1_text[:-1]
                    elif focus == "p2" and p2_text:
                        p2_text = p2_text[:-1]

                else:
                    ch = ev.unicode
                    if ch and ch.isprintable():
                        if focus == "p1" and len(p1_text) < 20:
                            p1_text += ch; cursor_on = True
                        elif focus == "p2" and mode == "1" and len(p2_text) < 20:
                            p2_text += ch; cursor_on = True

        if needs_redraw:
            _draw_menu(*pygame.mouse.get_pos())

        clock.tick(60)

# ─────────────────────────────────────────────────────────────────────────────
#  PLAYER MOVE
# ─────────────────────────────────────────────────────────────────────────────

def ui_player_move(board, current_name, symbol,
                   p1_name, p1_score, p2_name, p2_score, draws):
    """
    Wait for a valid board click or Abandon Hope.
    Returns "reset" or None (move placed).
    """
    pygame.event.clear()

    def _draw():
        draw_game_window(board, p1_name, p1_score, p2_name, p2_score, draws)
        lbl    = F_QUOTE.render(f"{current_name}'s turn  –  click a square", True, C_YELLOW)
        shadow = F_QUOTE.render(f"{current_name}'s turn  –  click a square", True, C_DARK)
        tx = W // 2 - lbl.get_width() // 2
        screen.blit(shadow, (tx + 1, H - 88 + 1))
        screen.blit(lbl,    (tx,     H - 88))
        pygame.display.flip()

    _draw()

    while True:
        redraw = False
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if ev.type == pygame.MOUSEMOTION:
                # Only redraw if hovering the Abandon Hope button (colour changes)
                over = _RESET_RECT.collidepoint(ev.pos)
                prev = _RESET_RECT.collidepoint(ev.pos[0] - ev.rel[0],
                                                ev.pos[1] - ev.rel[1])
                if over != prev:
                    redraw = True

            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                mx, my = ev.pos

                if _RESET_RECT.collidepoint(mx, my):
                    board[:] = [str(i) for i in range(1, 10)]
                    randomize_background()
                    pygame.event.clear()
                    return "reset"

                col = min(mx // (W // 3), 2)
                row = min(my // (H // 3), 2)
                idx = row * 3 + col
                if board[idx] not in (SYM_X, SYM_O):
                    board[idx] = symbol
                    return None

        if redraw:
            _draw()

        clock.tick(60)

# ─────────────────────────────────────────────────────────────────────────────
#  MARVIN THINKING
# ─────────────────────────────────────────────────────────────────────────────

def ui_marvin_thinking(board, quote,
                       p1_name, p1_score, p2_name, p2_score, draws,
                       delay_ms=1800):
    """Show Marvin's quote banner for delay_ms ms, drawn once."""
    # Draw once then just wait
    draw_game_window(board, p1_name, p1_score, p2_name, p2_score, draws,
                     marvin_quote=quote)
    deadline = pygame.time.get_ticks() + delay_ms
    while pygame.time.get_ticks() < deadline:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        clock.tick(30)

# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT GUARD
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import subprocess
    pygame.quit()
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(here, "game_play.py")])
