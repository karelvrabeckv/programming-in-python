from pytest import fixture
from numpy.testing import assert_equal
from PIL import Image

import graphic_editor.graphic_editor as ge
import graphic_editor.kernels as ke
import numpy as np

# Fixtures

@fixture
def img():
    return np.asarray(Image.open('tests/lenna.png'), dtype=np.float)

@fixture
def rotate():
    return np.asarray(Image.open('tests/rotate.png'), dtype=np.uint8)

@fixture
def mirror():
    return np.asarray(Image.open('tests/mirror.png'), dtype=np.uint8)

@fixture
def inverse():
    return np.asarray(Image.open('tests/inverse.png'), dtype=np.uint8)

@fixture
def bw():
    return np.asarray(Image.open('tests/bw.png'), dtype=np.uint8)

@fixture
def lighten():
    return np.asarray(Image.open('tests/lighten.png'), dtype=np.uint8)

@fixture
def darken():
    return np.asarray(Image.open('tests/darken.png'), dtype=np.uint8)

@fixture
def sharpen():
    return np.asarray(Image.open('tests/sharpen.png'), dtype=np.uint8)

@fixture
def blur():
    return np.asarray(Image.open('tests/blur.png'), dtype=np.uint8)

@fixture
def edges():
    return np.asarray(Image.open('tests/edges.png'), dtype=np.uint8)

@fixture
def emboss():
    return np.asarray(Image.open('tests/emboss.png'), dtype=np.uint8)

@fixture
def unsharpmask():
    return np.asarray(Image.open('tests/unsharpmask.png'), dtype=np.uint8)

# Tests

def test_rotate(img, rotate):
    assert_equal(rotate, ge.rotate(img))

def test_mirror(img, mirror):
    assert_equal(mirror, ge.mirror(img))

def test_inverse(img, inverse):
    assert_equal(inverse, ge.inverse(img))

def test_bw(img, bw):
    assert_equal(bw, ge.bw(img))

def test_lighten(img, lighten):
    assert_equal(lighten, ge.lighten(img, str(50)))

def test_darken(img, darken):
    assert_equal(darken, ge.darken(img, str(50)))

def test_sharpen(img, sharpen):
    assert_equal(sharpen, ge.convolution(img, ke.sharpen_kernel))

def test_blur(img, blur):
    assert_equal(blur, ge.convolution(img, ke.blur_kernel))

def test_edges(img, edges):
    assert_equal(edges, ge.convolution(img, ke.edges_kernel))

def test_emboss(img, emboss):
    assert_equal(emboss, ge.convolution(img, ke.emboss_kernel))

def test_unsharpmask(img, unsharpmask):
    original = img.copy()
    original = ge.convolution(original, ke.identity_kernel)
    img = ge.convolution(img, ke.blur_kernel)
    assert_equal(unsharpmask, ge.unsharpmask(img, original, str(10)))
