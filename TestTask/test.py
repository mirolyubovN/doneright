from  __future__  import  absolute_import , print_function
import sys, xmltodict,json, time, xml.etree.ElementTree as ET, yaml
# from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# opening file and reading test plan
def openFile(arg):
    with open(arg) as file:
        try:
            if(str(arg).endswith('.json')):
                plan = json.load(file)
                # print(plan)
        # elif (str(arg).endswith('.xml')):
        #         isXml = True
        #         tree = etree.parse(arg)
        #         plan=json.dumps(xmltodict.parse(ET.tostring(tree.getroot()).decode()))
        #         # print ("1")
        #         # print (plan)
        #         plan=(xmltodict.parse(ET.tostring(tree.getroot()).decode())['root'])
        #         # print("2")
        #         # print(plan)
        #         plan=json.loads(json.dumps(plan))
        #         print("3")
        #         print(plan)
            elif (str(arg).endswith('.yaml')):
                plan = yaml.load(file)
            else:
                print("Format not supported")
                exitCode = 3
                print("Exited with exit code " + str(exitCode))
                exit(exitCode)
        except Exception:
            print ("Could not open file")
            exitCode = 1
            print ("Exited with exit code " + str(exitCode))
            exit(exitCode)
        return plan

# function that initiates a webdriver (Chrome in this case; the webdriver needs to be installed)
def startWebDriver():
    print ('Starting the driver')
    global driver
    options = Options()
    options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(chrome_options=options)
    print ('Driver launched')


def openSite(url):
    try:
        driver.get(url)
        time.sleep(3)
        opened="yes"
    except Exception:
        opened="no"
        # exitCode = 2
    finally:
        return opened

def getNode(location, nodeName):
    try:
        globals()[nodeName] = driver.find_element_by_xpath(location)
        result="yes"
    except Exception:
        result="no"
        print ("Failed")
        # exitCode = 3
    finally:
        return result

def getText(node):
    try:
        name = node.get_attribute('text')
    except Exception:
        # exitCode = 4
        name="Failed"
    finally:
        return name

def clickSomething(node):
    try:
        time.sleep(2)
        node.click()
        clicked="yes"
        time.sleep(2)
    except Exception:
        # exitCode = 5
        clicked="no"
    finally:
        return clicked

def execJS(js):
    try:
        driver.execute_script(js)
        executed="yes"
        time.sleep(5)
    except Exception:
        print ('JS ERROR')
        # exitCode = 6
        executed="no"
    finally:
        return executed

def executeStep(actionStep):
    global driver
    global nodeName
    print ('Executing action :')


    if(actionStep.get('open')):
        print ('Opening website')
        return [{'opened':openSite(actionStep.get('open'))}]


    if (actionStep.get('getNode')):
        print ('Getting node')
        nodeName = str(actionStep.get('getNode').split(',')[1].strip())
        print("Node : "+ str(nodeName))
        # This should make the node to be stored in a variable named as the value of variable nodename
        node = getNode(actionStep.get('getNode').split(',')[0].strip(),nodeName)
        return [{nodeName:node}]


    if (actionStep.get('getText')):
        print ('Getting text of node')
        globals()[globals()[nodeName]] = getText(globals()[nodeName])
        print (globals()[globals()[nodeName]])
        return [{'text':getText(globals()[nodeName])}]


    if (actionStep.get('click')):
        print ('Initiating a click')
        # print(globals()[nodeName])
        print ("Clicking")
        return [{"click":clickSomething(globals()[nodeName])}]


    if (actionStep.get('exec')):
        print('Executing JS')
        return [{"exec": execJS(actionStep.get('exec'))}]


# check equality of two arrays
def assertEquals(expectedResult, actualValue):
    if(expectedResults==actualValue):
        print("Assertion passed")
    else:
        print("Assertion failed")
        exitCode=1

arguments = iter(sys.argv)
next(arguments)
# global isXml
# isXml= False
global exitCode
exitCode=0
for arg in arguments:
    print("Test file : "+str(arg))
    plan=openFile(arg)
    # if not isXml:
    scriptNumber = 0
    for script in plan["testPlan"]:
        scriptNumber+=1
        print("Script # " +str(scriptNumber))
        testCaseNumber=0
        for testCase in script["testScript"]:
            exitCode = 0
            testCaseNumber+=1
            # print('Test case' + str(testCaseNumber))
            result=[]
            # print("test case" + str(testCase))
            allSteps=testCase.get("testCase").get("actionSteps")
            # print("Steps:   " + str(allSteps))
            expectedResults = testCase.get("testCase").get("assertEquals")
            # print("Expected results: " +str(expectedResults))
            startWebDriver()
            for item in allSteps:
                result+=(executeStep(item))
            driver.quit()
            print("Expected: "+ str(expectedResults))
            print("Results: " + str(result))
            assertEquals(expectedResults,result)
            print ("Exited with exit code " + str(exitCode))
exit(exitCode)
    # else:
    #     plan = plan






