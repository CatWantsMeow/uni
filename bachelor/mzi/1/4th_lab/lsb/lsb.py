from PIL import Image
from argparse import ArgumentParser


source_image_filename = "../media/image.png"
destination_image_filename = "../media/changed_image.png"


def apply_mask(value, mask):
    return value >> len(mask) << len(mask) | int(mask, 2)


def extract_mask(value, mask_len):
    value &= 0xff >> (8 - mask_len)
    return "{0:0>{1}}".format(bin(value)[2:], mask_len)


def hide(data, hided=2):
    data = bytearray(data)
    bits = "".join("{:0>8}".format(bin(byte)[2:]) for byte in data) + "0" * 8
    image = Image.open(source_image_filename)
    pixels = image.load()
    bit_no = 0
    try:
        for i in xrange(image.size[0]):
            for j in xrange(image.size[1]):
                pixel = list(pixels[i, j])
                for index, color in enumerate(pixel):
                    pixel[index] = apply_mask(color, bits[bit_no: bit_no + hided])
                    bit_no += hided
                    if bit_no >= len(bits):
                        break
                pixels[i, j] = tuple(pixel)
                if bit_no >= len(bits):
                    raise StopIteration
    except StopIteration:
        pass
    image.save(destination_image_filename)


def show(hided=2):
    image = Image.open(destination_image_filename)
    bits = ""
    pixels = image.load()
    try:
        for i in xrange(image.size[0]):
            for j in xrange(image.size[1]):
                for color in pixels[i, j]:
                    bits += extract_mask(color, hided)
                    if bits[-8:] == "0" * 8:
                        raise StopIteration
    except StopIteration:
        pass

    bit_no = 0
    data = bytearray()
    while bit_no < len(bits[:-8]):
        data.append(int(bits[bit_no: bit_no + 8], 2))
        bit_no += 8
    return str(data)


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--show", action="store_true")
    arg_parser.add_argument("--hide", action="store_true")
    args = arg_parser.parse_args()

    if args.show:
        print show()

    if args.hide:
        data = raw_input()
        hide(data)


if __name__ == '__main__':
    main()