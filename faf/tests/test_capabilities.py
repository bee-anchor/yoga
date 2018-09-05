import pytest
from unittest.mock import patch
from argparse import Namespace
import faf.capabilities
import tempfile


class TestCapabilities:

    @pytest.fixture(autouse=True)
    def cap_file_setup(self):
        file = tempfile.NamedTemporaryFile()
        file.write(
        b'''[windows10chrome]
        browserName = chrome
        platform = Windows 10
        version = 68.0
        
        [android6]
        platformName = Android
        platformVersion = 6.0
        deviceName = Android Emulator
        browserName = Browser
        ''')
        file.flush()
        self.temp_caps_file = file.name
        yield
        file.close()

    def test_get_local_caps(self):
        args = Namespace(local_capabilities_file=self.temp_caps_file, capability='android6')
        caps = faf.capabilities.Capabilities(args).get_local_capabilities()
        expected_caps = {
            'platformName': 'Android',
            'platformVersion': '6.0',
            'deviceName': 'Android Emulator',
            'browserName': 'Browser'
        }
        assert caps == expected_caps

    def test_get_local_caps_raises_error_for_unknown_caps(self):
        args = Namespace(local_capabilities_file=self.temp_caps_file, capability='andrude6')
        with pytest.raises(KeyError, match='Local capabilities config does not have section for selection: andrude6'):
            faf.capabilities.Capabilities(args).get_local_capabilities()


    def test_get_remote_caps(self):
        args = Namespace(capability='windows10chrome')
        with patch('faf.capabilities.os') as mock_os:
            mock_os.path.join.return_value = self.temp_caps_file
            caps = faf.capabilities.Capabilities(args).get_remote_capabilities()
        expected_caps = {
            'platform': 'Windows 10',
            'version': '68.0',
            'browserName': 'chrome'
        }
        assert caps == expected_caps

    def test_get_remote_caps_raises_error_for_unknown_caps(self):
        args = Namespace(capability='windows10unknown')
        with patch('faf.capabilities.os') as mock_os:
            mock_os.path.join.return_value = self.temp_caps_file
            with pytest.raises(KeyError, match='Remote capabilities config does not have section for selection: windows10unknown'):
                faf.capabilities.Capabilities(args).get_remote_capabilities()
        
    def test_get_formatted_local_caps(self):
        args = Namespace(local_capabilities_file=self.temp_caps_file, capability='android6')
        caps = faf.capabilities.Capabilities(args).get_formatted_local_capabilities()
        expected_caps = 'platformName: Android, platformVersion: 6.0, deviceName: Android Emulator, browserName: Browser'
        assert caps == expected_caps

    def test_get_formatted_remote_caps(self):
        args = Namespace(capability='windows10chrome')
        with patch('faf.capabilities.os') as mock_os:
            mock_os.path.join.return_value = self.temp_caps_file
            caps = faf.capabilities.Capabilities(args).get_formatted_remote_capabilities()
        expected_caps = 'browserName: chrome, platform: Windows 10, version: 68.0'
        assert caps == expected_caps
