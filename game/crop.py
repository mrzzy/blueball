from PIL import Image

IDLE_SPRITES_PATH = [
    "game/assets/monk/idle/idle_1.png",
    "game/assets/monk/idle/idle_2.png",
    "game/assets/monk/idle/idle_3.png",
    "game/assets/monk/idle/idle_4.png",
    "game/assets/monk/idle/idle_5.png",
    "game/assets/monk/idle/idle_6.png",
]

RUN_SPRITES_PATH = [
    "game/assets/monk/run/run_1.png",
    "game/assets/monk/run/run_2.png",
    "game/assets/monk/run/run_3.png",
    "game/assets/monk/run/run_4.png",
    "game/assets/monk/run/run_5.png",
    "game/assets/monk/run/run_6.png",
    "game/assets/monk/run/run_7.png",
    "game/assets/monk/run/run_8.png",
]

JUMP_UP_SPRITES_PATH = [
    "game/assets/monk/j_up/j_up_1.png",
    "game/assets/monk/j_up/j_up_2.png",
    "game/assets/monk/j_up/j_up_3.png",
]

JUMP_DOWN_SPRITES_PATH = [
    "game/assets/monk/j_down/j_down_1.png",
    "game/assets/monk/j_down/j_down_2.png",
    "game/assets/monk/j_down/j_down_3.png",
]

KICK_SPRITES_PATH = [
    "game/assets/monk/air_atk/air_atk_1.png",
    "game/assets/monk/air_atk/air_atk_2.png",
    "game/assets/monk/air_atk/air_atk_3.png",
    "game/assets/monk/air_atk/air_atk_4.png",
    "game/assets/monk/air_atk/air_atk_5.png",
    "game/assets/monk/air_atk/air_atk_6.png",
    "game/assets/monk/air_atk/air_atk_7.png",
]

images = []
images.append(IDLE_SPRITES_PATH)
images.append(KICK_SPRITES_PATH)
images.append(JUMP_DOWN_SPRITES_PATH)
images.append(JUMP_UP_SPRITES_PATH)
images.append(RUN_SPRITES_PATH)


for i in range(len(images)):
    for j in range(len(images[i])):
        im = Image.open(images[i][j])
        im2 = im.crop(im.getbbox())
        im2.save(images[i][j])