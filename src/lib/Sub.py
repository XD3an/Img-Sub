from PIL import Image
from pwn import *
import random

class ImgSub:
    def __init__(self) -> None:
        self.img = None
        self.img_path = None
        self.width = None
        self.height = None
        # self.message = None

    def load(self, img_path: str) -> None:
        if img_path:
            self.img = Image.open(img_path).convert('RGB')   # for simplicity, convert to RGB
            self.img_path = img_path
            self.width, self.height = self.img.size
            log.success(f'Image loaded from {img_path}')
        else:
            log.failure(f'Please input your message and the path of the image file.')

    def encode_by_text(self, message: str, output_path: str, levels: list, channel: str = 'R') -> None:
        # message process
        self.message = message
        # add eof
        binary_message = ''.join(format(b, '08b') for b in message.encode('utf-8'))
        # log.info(f'Binary message: {binary_message}')
        log.info(f'Binary message length: {len(binary_message)}')
        if len(binary_message) > self.width * self.height:
            raise ValueError("Message is too long to be encoded in the image.")
        # channel process
        channel = 0 if channel == 'R' else 1 if channel == 'G' else 2 if channel == 'B' else 0

        # encode process
        index = 0
        for i in range(self.width):
            for j in range(self.height):
                pixel = list(self.img.getpixel((i, j)))
                # level=0, 1, 2, 3, 4, 5, 6, 7
                # level=0, 0b11111110
                # level=1, 0b11111101
                # level=2, 0b11111011
                # level=3, 0b11110111
                # level=4, 0b11101111
                # level=5, 0b11011111
                # level=6, 0b10111111
                # level=7, 0b01111111
                # pixel[channel] = (pixel[channel] & (0b11111111 & ~(0b1 << level))) | int(binary_message[index]) << level
                for level in levels:
                    pixel[channel] = (pixel[channel] & (0b11111111 & ~(0b1 << level))) | int(binary_message[index]) << level
                # pixel[0] = (pixel[0] & (0b11111111 & ~(0b1 << level))) | int(binary_message[index]) << level # R
                # pixel[1] = (pixel[1] & (0b11111111 & ~(0b1 << level))) | int(binary_message[index]) << level # G
                # pixel[2] = (pixel[2] & (0b11111111 & ~(0b1 << level))) | int(binary_message[index]) << level # B
                index += 1
                self.img.putpixel((i, j), tuple(pixel))

                if index >= len(binary_message):
                    break
            if index >= len(binary_message):
                break

        self.img.save(output_path)
        log.success(f'Image saved as {output_path}')

    def decode_for_text(self, level: int, channel: str = 'R', decode_size: int = 1) -> str:
        binary_message = ''
        # channel process
        channel = 0 if channel == 'R' else 1 if channel == 'G' else 2 if channel == 'B' else 0

        # decode process
        for i in range(self.width):
            for j in range(self.height):
                pixel = self.img.getpixel((i, j))
                binary_message += str((pixel[channel] >> level) & 0b1)
                # binary_message += str((pixel[0] >> level) & 0b1) # R
                # binary_message += str((pixel[1] >> level) & 0b1) # G
                # binary_message += str((pixel[2] >> level) & 0b1) # B
                if len(binary_message) >= decode_size * 8:
                    break
            if len(binary_message) >= decode_size * 8:
                break

        # convert binary message to string
        message = bytes(int(binary_message[i: i + 8], 2) for i in range(0, len(binary_message), 8)).decode('utf-8', errors='ignore')
        return message

    def encode_by_watermark(self, watermark_path: str, output_path: str, levels: list, channel: str = 'R') -> None:
        watermark = Image.open(watermark_path).convert('1')  # convert image to black and white
        # watermark = watermark.resize((self.width, self.height))
        watermark_width, watermark_height = watermark.size
        # channel process
        channel = 0 if channel == 'R' else 1 if channel == 'G' else 2 if channel == 'B' else 0

        # watermark to image process
        if watermark_width > self.width or watermark_height > self.height:
            raise ValueError("Watermark is too large to be encoded in the image.")

        # random position for hiding watermark
        random_number = random.randint(0, max(self.width, self.height) - max(watermark_width, watermark_height))
        # print(random_number)    

        # random to hide watermark
        for i in range(watermark_width):
            for j in range(watermark_height):
                # pixel = list(self.img.getpixel((i, j)))
                pixel = list(self.img.getpixel((i + random_number, j + random_number)))
                watermark_pixel = watermark.getpixel((i, j))
                watermark_pixel = 0 if watermark_pixel < 128 else 1
                # level=0, 1, 2, 3, 4, 5, 6, 7
                # level=0, 0b11111110
                # level=1, 0b11111101
                # level=2, 0b11111011
                # level=3, 0b11110111
                # level=4, 0b11101111
                # level=5, 0b11011111
                # level=6, 0b10111111
                # level=7, 0b01111111
                # pixel[channel] = (pixel[channel] & (0b11111111 & ~(0b1 << level))) | watermark_pixel << level
                for level in levels:
                    pixel[channel] = (pixel[channel] & (0b11111111 & ~(0b1 << level))) | watermark_pixel << level
                # pixel[0] = (pixel[0] & (0b11111111 & ~(0b1 << level))) | watermark_pixel << level # R
                # pixel[1] = (pixel[1] & (0b11111111 & ~(0b1 << level))) | watermark_pixel << level # G
                # pixel[2] = (pixel[2] & (0b11111111 & ~(0b1 << level))) | watermark_pixel << level # B
                # self.img.putpixel((i, j), tuple(pixel))
                self.img.putpixel((i + random_number, j + random_number), tuple(pixel))

        self.img.save(output_path)
        log.success(f'Image saved as {output_path}')

    def decode_for_watermark(self, des_watermark_path: str, level: int, channel: str = 'R') -> None:
        watermark = Image.new('1', (self.width, self.height))
        # channel process
        channel = 0 if channel == 'R' else 1 if channel == 'G' else 2 if channel == 'B' else 0

        for i in range(self.width):
            for j in range(self.height):
                pixel = self.img.getpixel((i, j))
                watermark.putpixel((i, j), (pixel[channel] >> level) & 0b1)
                # watermark.putpixel((i, j), (pixel[0] >> level) & 0b1) # R
                # watermark.putpixel((i, j), (pixel[1] >> level) & 0b1) # G
                # watermark.putpixel((i, j), (pixel[2] >> level) & 0b1) # B

        watermark.save(des_watermark_path)
        log.success(f'Watermark saved as {des_watermark_path}')