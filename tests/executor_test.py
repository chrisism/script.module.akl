import unittest, os
from unittest.mock import Mock, patch, MagicMock

import logging
from lib.akl.launchers import LauncherABC

from lib.akl.executors import AndroidActivityExecutor, ExecutorFactory, ExecutorSettings

logger = logging.getLogger(__name__)
logging.basicConfig(format = '%(asctime)s %(module)s %(levelname)s: %(message)s',
                datefmt = '%m/%d/%Y %I:%M:%S %p', level = logging.DEBUG) 

class Test_executortests(unittest.TestCase):
    
    @patch('lib.akl.executors.io.is_windows')
    @patch('lib.akl.executors.io.is_linux')            
    def test_if_on_linux_factory_loads_with_correct_executor(self, is_linux_mock:MagicMock, is_windows_mock:MagicMock):
        
        # arrange
        is_linux_mock.return_value = True
        is_windows_mock.return_value = False
        
        launcherPath = 'path/to/app'
        settings = ExecutorSettings()

        # act
        factory = ExecutorFactory(None, settings)
        executor = factory.create(launcherPath)
        
        # assert
        actual = executor.__class__.__name__
        expected = 'LinuxExecutor'
        assert actual == expected
                
    @patch('lib.akl.executors.io.is_windows')
    @patch('lib.akl.executors.io.is_osx')
    @patch('lib.akl.executors.io.is_linux')                   
    def test_if_on_windows_factory_loads_with_correct_executor(self, is_linux_mock:MagicMock, is_osx_mock:MagicMock, is_windows_mock:MagicMock):
        
        # arrange
        is_linux_mock.return_value = False
        is_windows_mock.return_value = True
        is_osx_mock.return_value = False

        launcherPath = 'c:\\app\\testcase.exe'
        settings = ExecutorSettings()

        # act
        factory = ExecutorFactory(None, settings)
        executor = factory.create(launcherPath)
        
        # assert
        actual = executor.__class__.__name__
        expected = 'WindowsExecutor'
        assert actual == expected  
        
    @patch('lib.akl.executors.io.is_windows')
    @patch('lib.akl.executors.io.is_osx')
    @patch('lib.akl.executors.io.is_linux')               
    def test_if_on_windows_with_bat_files_factory_loads_with_correct_executor(self, is_linux_mock:MagicMock, is_osx_mock:MagicMock, is_windows_mock:MagicMock):

        # arrange
        is_linux_mock.return_value = False
        is_windows_mock.return_value = True
        is_osx_mock.return_value = False
                
        launcherPath = 'c:\\app\\testcase.bat'
        settings = ExecutorSettings()

        # act
        factory = ExecutorFactory(None, settings)
        executor = factory.create(launcherPath)
        
        # assert
        actual = executor.__class__.__name__
        expected = 'WindowsBatchFileExecutor'
        assert actual == expected  
        
    @patch('lib.akl.executors.io.is_windows')
    @patch('lib.akl.executors.io.is_osx')
    @patch('lib.akl.executors.io.is_linux')      
    def test_if_on_windows_with_lnk_files_factory_loads_with_correct_executor(self, is_linux_mock:MagicMock, is_osx_mock:MagicMock, is_windows_mock:MagicMock):

        # arrange
        is_linux_mock.return_value = False
        is_windows_mock.return_value = True
        is_osx_mock.return_value = False
        
        launcherPath = 'c:\\app\\testcase.lnk'
        settings = ExecutorSettings()

        # act
        factory = ExecutorFactory(None, settings)
        executor = factory.create(launcherPath)

        # assert
        actual = executor.__class__.__name__
        expected = 'WindowsLnkFileExecutor'
        assert actual == expected
        
    def test_if_xbmc_apppath_factory_loads_with_correct_executor(self):
         
        # arrange        
        launcherPath = 'c:\\boop\\xbmc.exe'
        settings = ExecutorSettings()

        # act
        factory = ExecutorFactory(None, settings)
        executor = factory.create(launcherPath)

        # assert
        actual = executor.__class__.__name__
        expected = 'XbmcExecutor'
        assert actual == expected
        
    @patch('lib.akl.executors.io.is_windows')
    @patch('lib.akl.executors.io.is_osx')
    @patch('lib.akl.executors.io.is_linux')         
    def test_if_on_osx_factory_loads_with_correct_executor(self, is_linux_mock:MagicMock, is_osx_mock:MagicMock, is_windows_mock:MagicMock):

        # arrange
        is_linux_mock.return_value = False
        is_windows_mock.return_value = False
        is_osx_mock.return_value = True

        launcherPath = 'durp\\apple\\durp'
        settings = ExecutorSettings()

        # act
        factory = ExecutorFactory(None, settings)
        executor = factory.create(launcherPath)

        # assert
        actual = executor.__class__.__name__
        expected = 'OSXExecutor'
        assert actual == expected
       
    def test_when_using_urls_the_correct_web_executor_loads(self):
        
        # arrange
        launcherPath = 'steam://rungameid/'
        settings = ExecutorSettings()

        # act
        factory = ExecutorFactory(None, settings)
        executor = factory.create(launcherPath)

        # assert
        actual = executor.__class__.__name__
        expected = 'WebBrowserExecutor'
        assert actual == expected

    @patch("lib.akl.executors.xbmc.executebuiltin", autospec=True)
    def test_when_executing_on_android_it_has_the_correct_arguments(self, execute_mock: Mock):
        # arrange
        target = AndroidActivityExecutor()
        application = "com.nvidia.tegrazone3"
        args = []      
        kwargs = {
            "intent": "android.intent.action.VIEW",
            "dataURI": "nvidia://stream/target/4/124"
        }

        # act
        target.execute(application, *args, **kwargs)

        # assert
        assert execute_mock.called
        call = execute_mock.call_args_list[0]
        assert call.args[0] == 'StartAndroidActivity("com.nvidia.tegrazone3", "android.intent.action.VIEW", "", "nvidia://stream/target/4/124", "", "[]", "", "", "")'


if __name__ == '__main__':
    unittest.main()
