
def generate_matrix(*, size):
    import numpy as np
    
    if size <= 2:
        return np.matrix([[0, 2], [3, 1]])
    sub_matrix = generate_matrix(size=size / 2)
    return np.concatenate((
            np.concatenate((sub_matrix*4, sub_matrix*4+3), axis=0),
            np.concatenate((sub_matrix*4+2, sub_matrix*4+1), axis=0)), axis=1)

def main():

    import argparse
    from PIL import Image

    parser = argparse.ArgumentParser(description="A command-line tool for applying ordered dithering to images.")

    parser.add_argument(
        "source",
        type=str
    )

    parser.add_argument(
        "target",
        type=str
    )

    parser.add_argument(
        "--matsize",
        dest="matrix_size",
        nargs="?",
        const=8,
        default=8,
        type=int
    )

    args = parser.parse_args()

    index_matrix = generate_matrix(size=args.matrix_size)
    thrsh_matrix = (index_matrix + 0.5) / (index_matrix.shape[0] ** 2) * 255

    r_image = Image.open(args.source).convert("L")
    w_image = Image.new("1", r_image.size)

    mod_y, mod_x = thrsh_matrix.shape

    for y in range(r_image.size[1]):
        for x in range(r_image.size[0]):
            thrsh_value = thrsh_matrix[y % mod_y, x % mod_x]

            pixel_value = r_image.getpixel((x, y))
            w_image.putpixel((x, y), [0, 255][int(pixel_value > thrsh_value)])
    w_image.save(args.target)

    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
