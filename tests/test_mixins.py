# -*- coding: utf-8 -*-
from plexapi.utils import tag_singular

from . import conftest as utils

TEST_MIXIN_TAG = "Test Tag"
CUTE_CAT_SHA1 = "9f7003fc401761d8e0b0364d428b2dab2f789dbb"


def _test_mixins_tag(obj, attr, tag_method):
    add_tag_method = getattr(obj, "add" + tag_method)
    remove_tag_method = getattr(obj, "remove" + tag_method)
    field_name = tag_singular(attr)
    _tags = lambda: [t.tag for t in getattr(obj, attr)]
    _fields = lambda: [f for f in obj.fields if f.name == field_name]
    # Check tag is not present to begin with
    tags = _tags()
    assert TEST_MIXIN_TAG not in tags
    # Add tag and lock the field
    add_tag_method(TEST_MIXIN_TAG)
    obj.reload()
    tags = _tags()
    fields = _fields()
    assert TEST_MIXIN_TAG in tags
    assert fields and fields[0].locked
    # Remove tag and unlock to field to restore the clean state
    remove_tag_method(TEST_MIXIN_TAG, locked=False)
    obj.reload()
    tags = _tags()
    fields = _fields()
    assert TEST_MIXIN_TAG not in tags
    assert not fields


def edit_collection(obj):
    _test_mixins_tag(obj, "collections", "Collection")


def edit_country(obj):
    _test_mixins_tag(obj, "countries", "Country")


def edit_director(obj):
    _test_mixins_tag(obj, "directors", "Director")


def edit_genre(obj):
    _test_mixins_tag(obj, "genres", "Genre")


def edit_label(obj):
    _test_mixins_tag(obj, "labels", "Label")


def edit_mood(obj):
    _test_mixins_tag(obj, "moods", "Mood")


def edit_producer(obj):
    _test_mixins_tag(obj, "producers", "Producer")


def edit_similar_artist(obj):
    _test_mixins_tag(obj, "similar", "SimilarArtist")


def edit_style(obj):
    _test_mixins_tag(obj, "styles", "Style")


def edit_tag(obj):
    _test_mixins_tag(obj, "tags", "Tag")


def edit_writer(obj):
    _test_mixins_tag(obj, "writers", "Writer")


def _test_mixins_art_poster(obj, attr):
    cap_attr = attr[:-1].capitalize()
    get_img_method = getattr(obj, attr)
    set_img_method = getattr(obj, "set" + cap_attr)
    upload_img_method = getattr(obj, "upload" + cap_attr)
    images = get_img_method()
    if images:
        image = images[0]
        assert len(image.key) >= 10
        if not image.ratingKey.startswith(("default://", "media://", "upload://")):
            assert image.provider
        assert len(image.ratingKey) >= 10
        assert utils.is_bool(image.selected)
        assert len(image.thumb) >= 10
        if len(images) >= 2:
            # Select a different image
            set_img_method(images[1])
            images = get_img_method()
            assert images[0].selected is False
            assert images[1].selected is True
    # Test upload image from file
    upload_img_method(filepath=utils.STUB_IMAGE_PATH)
    images = get_img_method()
    file_image = [
        i for i in images
        if i.ratingKey.startswith('upload://') and i.ratingKey.endswith(CUTE_CAT_SHA1)
    ]
    assert file_image
    set_img_method(images[0])  # Reset to default image


def edit_art(obj):
    _test_mixins_art_poster(obj, 'arts')


def edit_poster(obj):
    _test_mixins_art_poster(obj, 'posters')
