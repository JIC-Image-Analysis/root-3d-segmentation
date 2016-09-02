"""Module for generating and parsing information from OME XML.

Uses showinf command below to generate the OME XML:

    showinf -nopix -omexml-only

The intent of the code is for the Python layer to abstract away the pain of
having to interact directly with XML.

Usage:

    omexml = OmeXml(microscopy_fpath)
    series3 = omexml.series(3)
    print series3.identifier, series3.name
    for child in series3.element:
        print child.tag, child.attrib

"""

import sys
from subprocess import Popen, PIPE

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

OME_SCHEMA = "{http://www.openmicroscopy.org/Schemas/OME/2016-06}"


def tag(name):
    """Return tag prefixed with OME schema."""
    return OME_SCHEMA + name


class Series(object):
    """Microscopy file series."""

    def __init__(self, element):
        self.element = element

    @property
    def identifier(self):
        """Return series identifier as an integer."""
        i_str = self.element.attrib["ID"]
        _, i = i_str.split(":")
        return int(i)

    @property
    def name(self):
        """Return series name."""
        return self.element.attrib["Name"]


class OmeXml(object):
    """Class for working with OME XML metadata."""

    def __init__(self, fpath):
        cmd = ["showinf", "-nopix", "-omexml-only", fpath]
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        self.xml, err = p.communicate()
        if err:
            raise(RuntimeError("\nshowinf issue:\n{}".format(err)))
        self.tree = ET.XML(self.xml)

    def series_iter(self):
        """Iterate over all the image series."""
        for s in self.tree.iter(tag("Image")):
            yield Series(s)

    def series(self, identifier):
        """Return a specific image series."""
        for s in self.series_iter():
            if s.identifier == identifier:
                return s
