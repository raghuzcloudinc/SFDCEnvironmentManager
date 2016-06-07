from xml.dom.minidom import parse
import xml.dom.minidom
import os, sys
import shutil

EmvMap = {"1" : "DevLocal", "2" : "DevMaj", "3" : "QA", "4" : "MajStg", "5" : "Ditto","6" : "Prod"}
TaskMap = {"1" : "Retrieve", "2" : "Merge Files", "3" : "TestDeploy", "4" : "Deploy"}
GitFilePath = "SFDCProject/src"

GitRepoPath = "C:\\03.SunrunSalesforceGithub\\SFDCProject\\src"
CurrentDir = os.path.dirname(os.path.realpath(__file__));
unpackage = ""
envFolder = ""


DirectoryMap = {"ApexClass" :  "classes","ApexComponent" : "components","ApexPage" : "pages","ApexTrigger" : "triggers",
                "Community" : "communities","ConnectedApp" : "connectedApps",
                "CustomApplication" : "applications","CustomLabels" : "labels","ValidationRule" : "objects", "CustomObject" : "objects","CustomSite" : "sites",
                "CustomTab" : "tabs","Flow" : "flows","HomePageComponent" : "homePageComponents","CustomField" : "objects", 
                "ListView" : "objects", "WebLink" : "objects", "HomePageLayout" : "homePageLayouts","PermissionSet" : "permissionsets",
                "Portal" : "portals","Queue" : "queues",
                "RemoteSiteSetting" : "remoteSiteSettings","StaticResource" : "staticresources",
                "Workflow" : "workflows","Settings" : "settings", "EmailTemplate": "email"}

FileExtensions = {"ApexClass" :  ".cls","ApexComponent" : ".component","ApexPage" : ".page","ApexTrigger" : ".trigger",
                "Community" : ".community","ConnectedApp" : ".connectedApp",
                "CustomApplication" : ".app","CustomLabels" : ".labels","ValidationRule" : ".object", "CustomObject" : ".object","CustomSite" : ".site",
                "CustomTab" : ".tab","Flow" : ".flow","HomePageComponent" : ".homePageComponent", "CustomField" :".object",
                "ListView" : ".object", "WebLink" :".object", "HomePageLayout" : ".homePageLayout", 
		"PermissionSet" : ".permissionset","Portal" : ".portal","Queue" : ".queue",
                "RemoteSiteSetting" : ".remoteSite","StaticResource" : ".resource",
                "Workflow" : ".workflow","Settings" : ".settings", "EmailTemplate" : ".email"}

MetaFileExtensions = {"ApexClass" :  ".cls-meta.xml", "ApexComponent" : ".component-meta.xml","ApexPage" : ".page-meta.xml",
                "ApexTrigger" : ".trigger-meta.xml","CustomTab" : "tabs","StaticResource" : ".resource-meta.xml", "EmailTemplate" : ".email-meta.xml" }


def createDir(parent):
    if not os.path.exists(parent):
    	os.makedirs(parent);
    return;

def deleteDir(parent):
    shutil.rmtree(parent, ignore_errors=True)
    return;

def coptyAllFiles(src, dst):
    shutil.copytree(src, dst, symlinks=False, ignore=None)
    return;

def coptyFile(srcFile, dstFile):
    shutil.copyfile(srcFile, dstFile)
    return;

def getFileName(fieldName):
    fileNameParts = fieldName.split('.');
    return fileNameParts[0];
    
def mergeFiles(sourceEnv, targetEnv):

	print "You have selected to merge files from " + sourceEnv + " to " + targetEnv;

	# Open XML document using minidom parser
	DOMTree = xml.dom.minidom.parse(envFolder + "\\package.xml")
	collection = DOMTree.documentElement
	typesList = collection.getElementsByTagName("types")
	
	for typeVal in typesList:

		membersList = typeVal.getElementsByTagName('members')
		if membersList.length > 0 :
			name = typeVal.getElementsByTagName('name')[0]
			nameVal = name.childNodes[0].data

			directoryName = DirectoryMap.get(nameVal);
			fileExtension = FileExtensions.get(nameVal);
			metalFileExtension = MetaFileExtensions.get(nameVal);

			for member in membersList:
				memberVal = member.childNodes[0].data
				if memberVal == "*":
					print ('Selected all files ...');
					#coptyAllFiles(GitRepoPath + "\\" + directoryName, unpackage + "\\" + directoryName);
					gitCommand = "git checkout " + sourceEnv;
					gitCommand += " " + directoryName + "/*";  
					os.system(gitCommand);
				else:

					if nameVal == "CustomField":
						memberVal = getFileName(memberVal);

					if (nameVal == "ValidationRule" or nameVal == "ListView" or nameVal == "WebLink"):
						if "." in memberVal: 
							memberVals = memberVal.split('.');
							memberVal = memberVals[0];

					gitCommand = "git checkout " + sourceEnv;
					sourceFile1 =  directoryName + "/" + memberVal + fileExtension
					gitCommand += " " + sourceFile1

					if metalFileExtension is not None:
						sourceFile2 = directoryName + "/" + memberVal + metalFileExtension
						gitCommand += " " + sourceFile2

					#print ("\n   Source File: " + gitCommand);
					os.system(gitCommand);

	return;


def createPackage():
	deleteDir(unpackage)
	createDir(unpackage)
	print ('Creating package in ' + unpackage);
	coptyFile(envFolder + "\\package.xml", unpackage + "\\package.xml");

	# Open XML document using minidom parser
	DOMTree = xml.dom.minidom.parse(envFolder + "\\package.xml")
	collection = DOMTree.documentElement
	typesList = collection.getElementsByTagName("types")

	for typeVal in typesList:
		membersList = typeVal.getElementsByTagName('members')
		if membersList.length > 0 :
			name = typeVal.getElementsByTagName('name')[0]
			nameVal = name.childNodes[0].data
			
			directoryName = DirectoryMap.get(nameVal);
			fileExtension = FileExtensions.get(nameVal);
			metalFileExtension = MetaFileExtensions.get(nameVal);
			createDir(unpackage + "\\" + directoryName)


			for member in membersList:
				memberVal = member.childNodes[0].data
				if memberVal == "*":
					deleteDir(unpackage + "\\" + directoryName)
					coptyAllFiles(GitRepoPath + "\\" + directoryName, unpackage + "\\" + directoryName);
				else:

					if nameVal == "CustomField":
						memberVal = getFileName(memberVal);

					if (nameVal == "ValidationRule" or nameVal == "ListView" or nameVal == "WebLink"):
						if "." in memberVal: 
							memberVals = memberVal.split('.');
							memberVal = memberVals[0];
						

					if "/" in memberVal: 
						memberVals = memberVal.split('/');
						innerFolder = memberVals[0];
						createDir(unpackage + "\\" + directoryName + "\\" + innerFolder);
						memberVal = memberVal.replace("/", "\\");

					sourceFile1 = GitRepoPath + "\\" + directoryName + "\\" + memberVal + fileExtension
					destFile1 = unpackage + "\\" + directoryName + "\\" + memberVal + fileExtension
					coptyFile(sourceFile1, destFile1);

					if metalFileExtension is not None:
						sourceFile2 = GitRepoPath + "\\" + directoryName + "\\" + memberVal + metalFileExtension
						destFile2 = unpackage + "\\" + directoryName + "\\" + memberVal + metalFileExtension
						coptyFile(sourceFile2, destFile2);
	return;


print ('\n   Task Names')
for key in range(1, 5):
    print '\t' + str(key) + "." + TaskMap.get(str(key));
taskNumber = input('   Enter Task# ')
selectedTask = TaskMap.get(str(taskNumber));

print ('   Sunrun SFDC Environments')
for key in range(1, 7):
    print '\t' + str(key)+"."+EmvMap.get(str(key));

	
sourceEnv = "";
targetEnv = "";
if selectedTask == "Merge Files":
	envSource = input('   Enter Source Environment# ')
	envTarget = input('   Enter Target Environment# ')

	sourceEnv = EmvMap.get(str(envSource));
	targetEnv = EmvMap.get(str(envTarget));
	envFolder = CurrentDir + "\\" + targetEnv.lower();

	if sourceEnv == "Prod":
		sourceEnv = "master";

	if targetEnv == "Prod":
		targetEnv = "master";
	
	print "Selected Source Environment: " + sourceEnv;
	print "Selected Target Environment: " + targetEnv;
else:
	envNaumber = input('   Enter Environment# ')
	selectedEnv = EmvMap.get(str(envNaumber));

	antTskName = selectedEnv + '_' + selectedTask;
	envFolder = CurrentDir + "\\" + selectedEnv.lower();
	unpackage = CurrentDir + "\\" + selectedEnv.lower() + "\\unpackage";

	print "Selected Environment: " + selectedEnv;
	print "Selected antTskName: " + antTskName;


	if selectedEnv == "Prod":
		selectedEnv = "master";

if selectedTask == "Merge Files":
	os.chdir(GitRepoPath);
	#os.system('REM git stash');
	os.system('git checkout -- *');
	os.system('git checkout ' + targetEnv);
	mergeFiles(sourceEnv, targetEnv);

elif selectedTask == "Retrieve":
	print "You have selected Retrieve";
	os.chdir(GitRepoPath);
	#os.system('REM git stash');
	os.system('git checkout -- *');
	os.system('git checkout ' + selectedEnv);

	os.chdir(CurrentDir);

	print 'ant ' + antTskName;
	os.system('ant ' + antTskName);

elif selectedTask == "TestDeploy":
	print "You have selected TestDeploy";

	os.chdir(GitRepoPath);
	os.system('REM git stash');
	os.system('git checkout ' + selectedEnv);

	os.chdir(CurrentDir);
	createPackage();
	confirmation = raw_input('   Please review the newly created package and confirm test deployment (Y\\N): ');

	print(confirmation);
	if str(confirmation) == "Y" or str(confirmation) == "y":
		os.system('ant ' + antTskName);
		print('Deploying the package ' + antTskName);

elif selectedTask == "Deploy":
	print "You have selected Deploy";
	os.chdir(GitRepoPath);
	os.system('REM git stash');
	os.system('git checkout ' + selectedEnv);

	os.chdir(CurrentDir);
	createPackage();
	confirmation = raw_input('   Please review the newly created package and confirm test deployment (Y\\N): ');

	print(confirmation);

	if str(confirmation) == "Y" or str(confirmation) == "y":
		os.system('ant ' + antTskName);
		print('Deploying the package ' + antTskName);
