from psychopy import visual, core, event
from psychtoolbox import WaitSecs
from events import EventMarker
from functions import *

# constants
FREQS = [130, 200, 280]
SEQ_LENS = [30, 36, 42]
TONE_LEN = 0.3

# ask for subject and block number
SUB_NUM = input("Input subject number: ")
BLOCK_NUM = input("Input block number: ")

# set subject number, block and seq_num as seed
SEED = int(SUB_NUM + "0" + BLOCK_NUM + str(seq_num))
print("Current seed: " + str(SEED))
random.seed(SEED)

# set up keyboard, window and RTBox
WIN = visual.Window(size = (1920, 1080),
    screen = -1,
    units = "norm",
    fullscr = False,
    pos = (0, 0),
    allowGUI = False)
KB = get_keyboard('Dell Dell USB Entry Keyboard')
MARKER = EventMarker()

# open log file
LOG = open_log(SUB_NUM, BLOCK_NUM)
score = get_score(LOG)
print(f"score: {score}")
seq_num = get_seq_num(LOG)
print(f"seq_num: {seq_num}")

# have subj listen the tones and display instructions if training block
if BLOCK_NUM == "0":
    hear_pitches(WIN, TONE_LEN, FREQS)
    instructions(WIN)
    SCORE_NEEDED = 3
else:
    welcome(WIN, BLOCK_NUM)
    SCORE_NEEDED = 18

# play sequences until SCORE_NEEDED is reached
while score < SCORE_NEEDED:
    target = get_target(FREQS)
    n_tones = get_n_tones(SEQ_LENS)

    # Play target
    n_target_plays = play_target(WIN, TONE_LEN, target)
    ready(WIN)
    WaitSecs(1)

    # Play tones
    fixation(WIN)
    WaitSecs(1)
    tone_nums, freqs, marks, is_targets, n_targets = play_sequence(MARKER, FREQS, TONE_LEN, target, n_tones)
    WIN.flip()
    WaitSecs(0.5)

    # Get response
    response = get_response(WIN)
    print(f'n_targets: {n_targets}')
    print(f'response: {response}')
    correct, score = update_score(WIN, n_targets, response, score, SCORE_NEEDED)
    print(f'score: {score}')
    seq_num += 1
    print(f'seq_num: {seq_num}')

    # Write log file
    write_log(LOG, n_tones, SEED, SUB_NUM, BLOCK_NUM, seq_num, target, n_target_plays, tone_nums,
              freqs, marks, is_targets, n_targets, response, correct, score)
    WaitSecs(1)

print("Block over.")

core.quit()
