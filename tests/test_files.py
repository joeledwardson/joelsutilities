import yaml
from joelsutilities import files
from pyfakefs.fake_filesystem_unittest import Patcher
import os


def test_get_filepaths():
    with Patcher() as patcher:
        # access the fake_filesystem object via patcher.fs
        patcher.fs.create_file('example_file_1', contents='test...')
        patcher.fs.create_file('example_file_2', contents='test...')
        patcher.fs.create_file('dir_a/dir_b/example_file_3', contents='test...')

        file_names = [os.path.basename(f) for f in files.get_filepaths('.')]
        assert 'example_file_1' in file_names
        assert 'example_file_2' in file_names

        assert files.get_filepaths('dir_a/dir_b', file_pattern='notwork') == []
        file_names = [
            os.path.basename(f)
            for f in files.get_filepaths('dir_a/dir_b', file_pattern='^example_file_.*$')
        ]
        assert file_names == ['example_file_3']

        assert files.get_filepaths('dir_a/dir_b', dir_pattern='notwork') == []
        assert len(files.get_filepaths('dir_a/dir_b', dir_pattern='^.*dir_b$')) == 1


def test_get_yaml_confs():
    with Patcher() as patcher:
        d1 = {'hello': 'there'}
        d2 = {'adios': 'amigo'}
        y1 = yaml.dump(d1)
        y2 = yaml.dump(d2)

        patcher.fs.create_file('config_1.yaml', contents=y1)
        patcher.fs.create_file('config_2.yaml', contents=y2)

        assert files.load_yaml_confs('.') == {
            'config_1': d1,
            'config_2': d2,
        }
