from PIL import Image
from paddleocr import PaddleOCR
from datetime import datetime
import logging
import cv2
import os

from paddleocr.ppocr.utils.logging import get_logger as ppocr_get_logger
ppocr_get_logger().setLevel(logging.ERROR)


class VideoCapture:
    CAPTURE_FRAME = 30

    cam = None
    cam_port = None

    def __init__(self, cam_port=0):
        self.cam_port = cam_port
        self.cam = cv2.VideoCapture(self.cam_port)

        self.cam.set(cv2.CAP_PROP_BRIGHTNESS, 60)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.cam.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        self.cam.set(cv2.CAP_PROP_FOCUS, 115)

    def capture_image(self, image_path):
        for i in range(self.CAPTURE_FRAME):
            temp = self.cam.read()
        result, image = self.cam.read()
        return cv2.imwrite(image_path, image) if result else False


class AirQualityOCR:
    image_name = None
    crop_root = None
    image_path = None
    done_root = None
    done_crop_root = None
    ocr = None
    image_crops = []

    DATA_POINTS = {
        # x-min, y-min, x-max, y-max
        'temperature': (120, 110, 220, 160),
        'humidity': (120, 175, 190, 220),
        'tvoc': (90, 245, 190, 290),
        'hcho': (240, 245, 340, 290),
        'pm2_5': (395, 115, 490, 160),
        'pm10': (395, 185, 490, 225),
        'co2': (395, 250, 490, 290),
    }

    @staticmethod
    def queue_images(queue_dir='images/queue/'):
        for file in os.listdir(queue_dir):
            filename = os.fsdecode(file)
            if filename.endswith(".png"):
                yield f'{queue_dir}{file}'

    def __ensure_dirs(self):
        if not os.path.exists(self.crop_root):
            os.makedirs(self.crop_root)
        if not os.path.exists(self.done_root):
            os.makedirs(self.done_root)
        if not os.path.exists(self.done_crop_root):
            os.makedirs(self.done_crop_root)

    def __init__(self, image_path, crop_root='images/crops/', done_root='images/done/', ocr=None):
        self.image_path = image_path
        self.image_name = os.path.basename(image_path)

        self.crop_root = crop_root
        self.done_root = done_root
        self.done_crop_root = f'{done_root}crops/'

        self.__ensure_dirs()

        self.ocr = ocr
        if not self.ocr:
            self.ocr = PaddleOCR(show_log=False, detector='aqi/inference/ch_PP-OCRv3_det_infer',
                                 det_model_dir='aqi/inference/ch_PP-OCRv3_det_infer',
                                 rec_model_dir='aqi/inference/ch_PP-OCRv3_rec_infer',
                                 table_model_dir='aqi/inference/ch_ppstructure_mobile_v2.0_SLANet_infer')

    def _create_crops(self):
        self.image_crops = []
        for data_point, bbox in self.DATA_POINTS.items():
            name_parts = self.image_name.split('.')
            crop_name = f'{self.crop_root}{name_parts[0]}_{data_point}.{name_parts[1]}'

            img = Image.open(self.image_path)
            img_crop = img.crop(bbox)
            img_crop.save(crop_name)

            self.image_crops.append((data_point, crop_name))

        return self.image_crops

    def archive_image(self):
        basename = os.path.basename(self.image_path)
        os.rename(self.image_path, f'{self.done_root}{basename}')

    def archive_crops(self):
        for data_point, img_crop in self.image_crops:
            basename = os.path.basename(img_crop)
            os.rename(img_crop, f'{self.done_crop_root}{basename}')

    def archive(self):
        self.archive_crops()
        self.archive_image()

    def get_capture_datestr(self):
        basename = os.path.basename(self.image_path)
        return os.path.splitext(basename)[0].split('_')[-1]

    def get_capture_time(self):
        return datetime.strptime(self.get_capture_datestr(), '%Y%m%d%H%M%S')

    def __cleanse_data_points(self, data_points):
        for key, data_point in data_points.items():
            if data_point:
                data_points[key] = ''.join(d for d in data_point if d.isdigit() or d in ['.'])
        return data_points

    def get_data_points(self):
        self._create_crops()

        data_points = {}
        for data_point, img_crop in self.image_crops:
            result = self.ocr.ocr(img_crop, cls=False)

            if result:
                data_points[data_point] = result[0][1][0]
            else:
                data_points[data_point] = None

        self.__cleanse_data_points(data_points)

        return data_points
