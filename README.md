# SFDCEnvironmentManager
SFDCEnvironmentManager: Batch file and directory structure to manage SFDC environments

Step-1: Install Source tree

Step-2: Clone Salesforce Github repository
	https://github.com/SunRun/salesforce.git

Step-3: Install Python version 2.7.* OR above 
	Modify the Path variables
	Execute python --version

Step-4: Install Ant and Force.com migration tool


Step-5: Download SFDCEnvironmentManager

	Modify the following fields in SFDCEnvironmentManager.py
		GitRepoPath

	Modify the following fields in build.properties
		git.folder
		dest.folder
		sfdcAnt.path
		