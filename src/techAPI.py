import os
from datetime import datetime
import random
from lib.Sub import ImgSub

techniques = ['m>i', 'w>i', 'm<i', 'w<i']

def generate_output_path() -> str:
    # generate output path
    output_path = f'./result/output_{datetime.now().strftime("%Y%m%d%H%M%S")}.png'
    # create directory if not exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    return output_path

def message_to_image(model: ImgSub, image: str, message: str, is_random: bool, size: int, output: str, level: str, channel: str) -> None:
    model.load(image)
    output = output if output else generate_output_path()
    # generate random size
    size = size if size else random.randint(1, 100)
    # level process
    levels = [int(i) for i in level.split(',')]
    # main process
    if message and not is_random:
        model.encode_by_text(message, output, levels, channel)
    else:
        # generate random binary bits with size
        random_message = ''.join([str(random.randint(0, 1)) for _ in range(size)])
        model.encode_by_text(random_message, output, levels, channel)

def image_to_message(model: ImgSub, image: str, decode_size: int, level: str, channel: str) -> str:
    # level process
    level = [int(i) for i in level.split(',')][0]
    # main process
    model.load(image)
    return model.decode_for_text(level, channel, decode_size)

def watermark_to_image(model: ImgSub, image: str, watermark: str, output: str, level: str, channel: str) -> None:
    # level process
    levels = [int(i) for i in level.split(',')]
    # main process
    model.load(image)
    output = output if output else generate_output_path()
    model.encode_by_watermark(watermark, output, levels, channel)

def image_to_watermark(model: ImgSub, image: str, output: str, level: str, channel: str) -> str:
    # level process
    level = [int(i) for i in level.split(',')][0]
    # main process
    model.load(image)
    if output:
        model.decode_for_watermark(output, level, channel)
    else:
        model.decode_for_watermark(generate_output_path(), level, channel)