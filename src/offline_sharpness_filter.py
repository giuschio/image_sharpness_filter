import argparse
import cv2
import numpy as np

from os.path import basename as basename

from utils import import_images, export_images


class OfflineSharpnessFilter():
    def __init__(self) -> None:
        self.images_in = None
        self.images_sharpness = None
        # size of downsampling window (higher is stricter)
        self.downsampling_factor = 10
        # between 0 (allow all images) and 100
        self.sharpness_threshold = 30
        self.sharp_images_indexes = list()

    def __calculate_sharpness(self):
        self.images_sharpness = list()
        for impath in self.images_in:
            image = cv2.imread(impath)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            self.images_sharpness.append(float(cv2.Laplacian(gray, cv2.CV_64F).var()))

    def import_images(self, image_dir) -> None:
        print("importing images...")
        self.images_in = import_images(fpath=image_dir)
        print("calculating sharpness...")
        self.__calculate_sharpness()

    def plot_sharpness_histogram(self) -> None:
        pass

    def filter_images(self):
        print("filtering...")
        sharpness_abs_threshold = float(np.percentile(self.images_sharpness, q=self.sharpness_threshold))
        self.sharp_images_indexes = list()
        i = 0
        while i + self.downsampling_factor < len(self.images_in):
            image_window = self.images_sharpness[i:i+self.downsampling_factor]
            argmax_in_window_index = np.argmax(image_window)
            argmax_global_index = argmax_in_window_index + i
            sharpness_amount = self.images_sharpness[argmax_global_index]
            if sharpness_amount < sharpness_abs_threshold:
                i += 1
            else:
                self.sharp_images_indexes.append(argmax_global_index)
                i += self.downsampling_factor

    def export_images(self, out_directory):
        print("exporting...")
        image_paths = [self.images_in[i] for i in self.sharp_images_indexes]
        export_images(image_paths, out_directory)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Absolute path to folder containing camera images.")
    parser.add_argument("output_dir", help="Absolute path to folder in which to export filtered images.")
    parser.add_argument("--downsampling_factor", help="Size of downsampling window.")
    parser.add_argument("--sharpness_threshold", help="Sharpnedd threshold: between 0 (allow all images) and 100.")
    args = parser.parse_args()

    filter = OfflineSharpnessFilter()
    filter.import_images(image_dir=str(args.input_dir))
    if args.downsampling_factor: filter.downsampling_factor = int(args.downsampling_factor)
    if args.sharpness_threshold: filter.sharpness_threshold = int(args.sharpness_threshold)
    filter.filter_images()
    filter.export_images(out_directory=str(args.output_dir))
    print("\n----------DONE-----------")
