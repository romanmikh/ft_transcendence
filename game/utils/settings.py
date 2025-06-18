# constants
WINDOW_WIDTH, WINDOW_HEIGHT     = 1000, 600

BALL_SPEED, PAD_SPEED           = 300, 1500
PAD_WIDTH, PAD_HEIGHT           = WINDOW_WIDTH//40, WINDOW_HEIGHT//4
TEXT_SIZE                       = WINDOW_HEIGHT//15
BALL_SIZE                       = PAD_WIDTH

POS = {
    'padl_start': (PAD_WIDTH // 2, WINDOW_HEIGHT // 2),
    'padr_start': (WINDOW_WIDTH - PAD_WIDTH // 2, WINDOW_HEIGHT // 2),
    'ball_start': (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2),
    'text_center': (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 10),
}