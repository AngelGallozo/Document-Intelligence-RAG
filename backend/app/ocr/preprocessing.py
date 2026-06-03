import cv2

from app.models.ocr_models import OCRProfile

def to_grayscale(image):

    return cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )


def enhance_contrast(image):

    return cv2.equalizeHist(
        image
    )


def denoise(image):

    return cv2.GaussianBlur(
        image,
        (3, 3),
        0
    )


def binarize(image):

    return cv2.adaptiveThreshold(
        image,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )


def preprocess_light(image):

    image = to_grayscale(image)

    return image


def preprocess_standard(image):

    image = to_grayscale(image)

    image = denoise(image)

    return image


def preprocess_aggressive(image):

    image = to_grayscale(image)

    image = denoise(image)

    image = binarize(image)

    return image


def preprocess_image(
    image_path: str,
    profile: OCRProfile = OCRProfile.STANDARD
):

    image = cv2.imread(image_path)

    if profile == OCRProfile.LIGHT:

        return preprocess_light(image)

    elif profile == OCRProfile.AGGRESSIVE:

        return preprocess_aggressive(image)

    return preprocess_standard(image)