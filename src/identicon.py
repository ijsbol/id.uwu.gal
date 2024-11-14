import hashlib

import cv2
from cv2.typing import MatLike
import numpy as np


__all__: tuple[str, ...] = (
    "generate_identicon",
)


def generate_identicon(identity: str, *, size: int = 7, scale: int = 40) -> MatLike:
    hashed_identity = hashlib.sha1(identity.encode('utf-8')).hexdigest()[:6 + (size * round(size / 2))]

    # Fetch RGB values from first 12 characters.
    foreground_r = int(hashed_identity[0:2], 16)
    foreground_g = int(hashed_identity[2:4], 16)
    foreground_b = int(hashed_identity[4:6], 16)

    # Create a new white background.
    height, width = size, size
    image = np.zeros((height, width, 3), np.uint8)
    image[:, :, 0] = 255
    image[:, :, 1] = 255
    image[:, :, 2] = 255

    # Draw the pixels
    active_pixels = [((int(c, 16) >> 1) % 2) for c in hashed_identity[6:]]
    active_pixel_coordinates = [(x, y) for x in range(size) for y in range(round(size / 2))]

    for i, (x, y) in enumerate(active_pixel_coordinates):
        if not active_pixels[i]:
            continue
        image[x, y] = [foreground_r, foreground_g, foreground_b]
        image[x, -y - 1] = [foreground_r, foreground_g, foreground_b]

    # Add padding
    # Resize image to 2-times scale to make padding easier.
    image = cv2.resize(image, (size*2, size*2), interpolation=cv2.INTER_AREA)
    padded_image = np.pad(
        image,
        ((1, 1), (1, 1), (0, 0)),
        mode='constant',
        constant_values=(
            (255, 255),
            (255, 255),
            (255, 255),
        ),
    )

    # Resize image to desired scale and return.
    return cv2.resize(padded_image, (size*scale, size*scale), interpolation=cv2.INTER_AREA)
