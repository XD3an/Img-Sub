import argparse
import pyfiglet
from pwn import *
from lib.Sub import ImgSub
from techAPI import *

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Image Steganography")
    parser.add_argument('-t', '--technique', type=str, help='Technique to use (message encode into image(m>i), watermark encode into image(w>i), message decoded by image(m<i), watermark decoded by image(w<i)), etc.')
    parser.add_argument('-i', '--image', type=str, help="Image file path")
    parser.add_argument('-m', '--message', type=str, help='The message to be processed')
    parser.add_argument('-o', '--output', type=str, help="Output file path (default: ./report/output_{datetime}.png)")
    parser.add_argument('-r', '--random', action='store_true', help="Random message")
    parser.add_argument('-s', '--size', type=int, help="Size of message")
    parser.add_argument('-w', '--watermark', type=str, help="Watermark file path")
    parser.add_argument('-d', '--decode_size', type=int, help="Size of message to decode", default=1)
    parser.add_argument('-l', '--levels', type=str, help="Level of Sub (bits position 7-0., e.g. 0,1,...) (default: 0 -> LSB)", default="0")
    parser.add_argument('-c', '--channel', type=str, help="Channel to use (r, g, b)", default='r')
    parser.add_argument('-v', '--verbose', action='store_true', help="Verbose mode")
    return parser.parse_args()

def banner() -> None:
    RED = "\33[91m"
    BLUE = "\33[94m"
    GREEN = "\033[32m"
    YELLOW = "\033[93m"
    PURPLE = '\033[0;35m' 
    CYAN = "\033[36m"
    END = "\033[0m"

    tmplr = f"""
    ┳     ┓ ┏┓  ┓ 
    ┃┏┳┓┏┓┣━┗┓┓┏┣┓
    ┻┛┗┗┗┫┛ ┗┛┗┻┗┛
        ┛        
    """

    ansi_shadow = """
    ██╗███╗   ███╗ ██████╗ ██╗  ███████╗██╗   ██╗██████╗ 
    ██║████╗ ████║██╔════╝ ╚██╗ ██╔════╝██║   ██║██╔══██╗
    ██║██╔████╔██║██║  ███╗ ╚██╗███████╗██║   ██║██████╔╝
    ██║██║╚██╔╝██║██║   ██║ ██╔╝╚════██║██║   ██║██╔══██╗
    ██║██║ ╚═╝ ██║╚██████╔╝██╔╝ ███████║╚██████╔╝██████╔╝
    ╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚══════╝ ╚═════╝ ╚═════╝ 
    """

    reverse = """
    =======================================================
    =    ===================  =======      ==========  ====
    ==  =====================  =====  ====  =========  ====
    ==  ======================  ====  ====  =========  ====
    ==  ===  =  = ====   ======  ====  =======  =  ==  ====
    ==  ===        ==  =  ======  =====  =====  =  ==    ==
    ==  ===  =  =  ===    =====  ========  ===  =  ==  =  =
    ==  ===  =  =  =====  ====  ====  ====  ==  =  ==  =  =
    ==  ===  =  =  ==  =  ===  =====  ====  ==  =  ==  =  =
    =    ==  =  =  ===   ===  =======      ====    ==    ==
    =======================================================
    """

    print(reverse)

def main() -> None:
    # print(pyfiglet.figlet_format('Img>Sub', font = 'lean', justify='center'))
    banner()
    log.success("Welcome to Img>Sub!")

    # init
    argv = parse_args()
    if argv.verbose:
        log.info(f'Arguments: {argv}')
    model = ImgSub()

    # main process
    if argv.technique not in techniques:
        log.failure("Invalid technique")
    else:
        if argv.technique == 'm>i':
            # message > image
            if argv.image:
                message_to_image(model, argv.image, argv.message, argv.random, argv.size, argv.output, argv.levels, argv.channel.upper())
            else:
                log.failure("Please input the path of the image file.")
        elif argv.technique == 'w>i':
            # watermark > image
            if argv.image and argv.watermark:
                watermark_to_image(model, argv.image, argv.watermark, argv.output, argv.levels, argv.channel.upper())
            else:
                log.failure("Please input the path of the image file and the watermark file.")
        elif argv.technique == 'm<i':
            # image > message
            if argv.image:
                decoded_message = image_to_message(model, argv.image, argv.decode_size, argv.levels, argv.channel.upper())
                log.success(f'Decoded message: \n\\__ {decoded_message}')
            else:
                log.failure("Please input the path of the image file.")
        elif argv.technique == 'w<i':
            # image > watermark
            if argv.image:
                image_to_watermark(model, argv.image, argv.output, argv.levels, argv.channel.upper())
            else:
                log.failure("Please input the path of the image file.")

if __name__ == '__main__':
    main()