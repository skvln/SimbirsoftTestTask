# SimbirsoftTestTask
Test task for Simbirsoft

# Execution
Before preparing the environment you need for *Java11*, *Python 3.9* and *Allure 2.19* to be installed.
1. Install Selenium Server. In my case, it was done by execution a standalone version. Be sure that Java is located at your PATH.
```CMD
java -jar selenium-server-4.5.3.jar standalone
```
2. Install required python packages by using pip:
```cmd
pip install -r requirements.txt
```
3. While Selenium server is running, execute *pytest* in test directory with alluredir argument:
```
pytest --alluredir /path/to/report/dir
```
4. To see test reports execute the Allure server. Path to a report directory should be the same as was given as pytest argument:
```
allure serve /path/to/report/dir
```
