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

        self.current = 0
        stack = self.get_stack()

        self.renderer = VolumeRenderer()
        self.renderer.make_volume_obj(stack, (1, 1, 1))

    def get_stack(self):
        return Image3D.from_directory(self.directories[self.current])


    def draw_hook(self):
        self.renderer.render(self.width, self.height, self.VMatrix, self.PMatrix)

    def reshape_hook(self):
        self.renderer.init_back_texture(self.width, self.height)

    def next_stack(self, x, y):
        self.current += 1
        if self.current == len(self.directories):
            self.current = 0
        stack = self.get_stack()
        self.renderer.volume_objects[0].update_stack(stack)

    def prev_stack(self, x, y):
        self.current -= 1
        if self.current < 0:
            self.current = len(self.directories) - 1
        stack = self.get_stack()
        self.renderer.volume_objects[0].update_stack(stack)

def visualise(directory):
    stack_visualiser = StackVisualiser("Root visualiser", 1000, 600)
    stack_visualiser.initialise(directory)

    stack_visualiser.zoom = 2.
    stack_visualiser.key_bindings["k"] = stack_visualiser.next_stack
    stack_visualiser.key_bindings["j"] = stack_visualiser.prev_stack

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
