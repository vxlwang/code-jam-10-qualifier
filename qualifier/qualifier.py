from PIL import Image

def valid_input(image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once.
    """
    x_divisive = image_size[0] % tile_size[0]
    y_divisive = image_size[1] % tile_size[1]

    if x_divisive != 0 or y_divisive != 0:
        return False

    n_tiles = (image_size[0] / tile_size[0]) * (image_size[1] / tile_size[1])

    if (len(set(ordering)) != len(ordering)) or (max(ordering) != n_tiles - 1) or (min(ordering) != 0):
        return False

    return True


def rearrange_tiles(image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each input tile exactly
    once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """
    img = Image.open(image_path)

    if not valid_input(img.size, tile_size, ordering):
        raise ValueError("The tile size or ordering are not valid for the given image")

    n_rows = img.size[1] // tile_size[1]
    n_cols = img.size[0] // tile_size[0]

    canvas = Image.new(img.mode, img.size)
    for i, target in enumerate(ordering):
        in_col = (i % n_cols) * tile_size[0]
        in_row = (i // n_cols) * tile_size[1]
        target_col = (target % n_cols) * tile_size[0]
        target_row = (target // n_cols) * tile_size[1]

        tile = img.crop((target_col, target_row, target_col+tile_size[0], target_row+tile_size[1]))
        canvas.paste(tile, (in_col, in_row))

    canvas.save(out_path)
