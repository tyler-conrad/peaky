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

def test_no_args_with_seperators(monkeypatch):
    patch_argv(monkeypatch, ['src/peaky.py', '--', '--'])

    from arg_split import ArgSplitter
    splitter = ArgSplitter()

    assert splitter.non_kivy_args() == ['--']
    assert splitter.kivy_args() == ['src/peaky.py']
    assert splitter.top_args() == []
    assert splitter.peaky_args() == ['src/peaky.py']

def test_no_args_extra_separators(monkeypatch):
    patch_argv(monkeypatch, ['src/peaky.py', '--', '--', '--'])

    from arg_split import ArgSplitter
    splitter = ArgSplitter()

    assert splitter.non_kivy_args() == ['--', '--']
    assert splitter.kivy_args() == ['src/peaky.py']
    assert splitter.top_args() == []
    assert splitter.peaky_args() == ['src/peaky.py', '--']

def test_one_arg(monkeypatch):
    arg_list = ['src/peaky.py']
    patch_argv(monkeypatch, arg_list) 

    from arg_split import ArgSplitter
    splitter = ArgSplitter()

    assert splitter.non_kivy_args() == []
    assert splitter.kivy_args() == arg_list
    assert splitter.top_args() == []
    assert splitter.peaky_args() == arg_list

def test_fancy_args(monkeypatch):
    arg_list = [
        'src/peaky.py',
        '-h',
        '--debug',
        '--auto-fullscreen',
        '--config', 'kivy:desktop:1',
        '-c', 'kivy:exit_on_escape:1',
        '-f',
        '--fake-fullscreen',
        '-w',
        '--provider', 'ccvtable1:tuio,192.168.0.1:3333',
        '-m', 'list',
        '--module=inspector',
        '-m', 'a,b,c',
        '--module=a,b,c',
        '--rotation=90',
        '-r', '90',
        '-s',
        '--size=640x480',
        '--dpi=96',
        '--',
        '-hv',
        '-bcHiSs',
        '-d', '34.34',
        '-n', '4848',
        '-U', 'user',
        '-p', '85858,84848',
        '-w', '8484',
        '--',
        '-i',
        '--help']
    patch_argv(monkeypatch, arg_list) 

    from arg_split import ArgSplitter
    splitter = ArgSplitter()

    assert splitter.non_kivy_args() == [
        '-hv',
        '-bcHiSs',
        '-d', '34.34',
        '-n', '4848',
        '-U', 'user',
        '-p', '85858,84848',
        '-w', '8484',
        '--',
        '-i',
        '--help']

    assert splitter.kivy_args() == [
        'src/peaky.py',
        '-h',
        '--debug',
        '--auto-fullscreen',
        '--config', 'kivy:desktop:1',
        '-c', 'kivy:exit_on_escape:1',
        '-f',
        '--fake-fullscreen',
        '-w',
        '--provider', 'ccvtable1:tuio,192.168.0.1:3333',
        '-m', 'list',
        '--module=inspector',
        '-m', 'a,b,c',
        '--module=a,b,c',
        '--rotation=90',
        '-r', '90',
        '-s',
        '--size=640x480',
        '--dpi=96']

    assert splitter.top_args() == [
        '-hv',
        '-bcHiSs',
        '-d', '34.34',
        '-n', '4848',
        '-U', 'user',
        '-p', '85858,84848',
        '-w', '8484']

    assert splitter.peaky_args() == [
        'src/peaky.py',
        '-i',
        '--help']

