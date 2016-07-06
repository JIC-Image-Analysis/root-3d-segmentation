"""Visualise 3D stacks."""

import os
import argparse

from jicbioimage.core.image import Image3D, _sorted_listdir
from pyvol.renderer import BaseGlutWindow, VolumeRenderer


class StackVisualiser(BaseGlutWindow):

    def initialise(self, directory):
        self.directories = [os.path.join(directory, d)
                            for d in _sorted_listdir(directory)
                            if d.endswith(".stack")]
        self.renderer = VolumeRenderer()
        stack = Image3D.from_directory(self.directories[0])
        self.renderer.make_volume_obj(stack, (1, 1, 1))

    def draw_hook(self):
        self.renderer.render(self.width, self.height, self.VMatrix, self.PMatrix)

    def reshape_hook(self):
        self.renderer.init_back_texture(self.width, self.height)


def visualise(directory):
    stack_visualiser = StackVisualiser("Root visualiser", 1000, 600)
    stack_visualiser.initialise(directory)
    stack_visualiser.zoom = 2.
    stack_visualiser.start()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory")
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        parser.error("Not a directory: " + args.directory)

    visualise(args.directory)


if __name__ == "__main__":
    main()
