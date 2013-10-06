# Copyright (c) Tyler Conrad.
# See LICENSE for details.

"""

"""
import sys

import pytest

def patch_argv(mp, argv):
    mp.setattr(sys, 'argv', argv)

def test_no_args(monkeypatch):
    patch_argv(monkeypatch, [])

    from arg_split import ArgSplitter
    splitter = ArgSplitter()
    
    assert splitter.non_kivy_args() == []
    assert splitter.kivy_args() == []
    assert splitter.top_args() == []
    with pytest.raises(IndexError):
        splitter.peaky_args()

def test_one_arg(monkeypatch):
    arg_list = ['src/peaky.py']
    patch_argv(monkeypatch, arg_list) 

    from arg_split import ArgSplitter
    splitter = ArgSplitter()

    assert splitter.non_kivy_args() == []
    assert splitter.kivy_args() == arg_list
    assert splitter.top_args() == []
    assert splitter.peaky_args() == arg_list

