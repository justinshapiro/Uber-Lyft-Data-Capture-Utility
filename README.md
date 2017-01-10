Uber/Lyft Data Capture Utility
==============================
### Manual & Installation Instructions ###

Overview
--------

The *Uber/Lyft Data Capture Utility* is a lightweight tool for Windows (Vista/7/8/8.1/10) and Mac OS X (10.10 – 10.12) that requests data from the Uber Rides and Lyft Rides APIs. Specifically, the tool collects data relating to price, surge multipliers, EAT (Estimated Arrival Time), and number of drivers (Lyft only) at each location (defined by longitude and latitude) for each Uber and Lyft product. Data is received by the program in the form of JSON objects and parsed into a CSV (Comma-Separated Values) file. The user interacts with the program via a GUI (Graphical User Interface) written in Java, but all the data collection is done by a “query_agent” background process written in Python. The user specifies the names and locations of the necessary input and output files within the GUI and the GUI launches the “query_agent” process with these names and locations in the form of absolute paths as parameters.

Installation
------------

1.	Although the program was written in Python and Java, you do not need to install the Python libraries or the JDK (Java Development Kit) nor the Uber Rides or Lyft Rides APIs to use this program. However, the program does use the standard Java runtime (like most programs do). To ensure a successful usage experience, please update your machine to the latest Java version. Links to the Java update can be found here: https://java.com/en/. 
2.	Download either **[Windows] Uber-Lyft_Data_Utility.zip** or **[Mac] Uber-Lyft_Data_Utility.zip**, depending on if you are planning on running the application on Windows or Mac.
3.	Extract the enclosed **Uber-Lyft_Data_Utility** folder to any location of your choosing. The location where you place this folder does not matter, as long as it is unzipped.
4.	That’s it, the entire program runs out of the Uber-Lyft_Data_Utility folder.

Using the Program
-----------------

 - The program exists as either one of these files:
	 - Windows: **Uber-Lyft Data Capture Utility.exe**
	 - Mac: **Uber-Lyft_Data_Capture_Utility.jar**
 - Double-click on either one of these files to launch the program. When the program appears, it will look like this:
 
 ![Screenshot of the Uber/Lyft Data Capture Utility](http://i.imgur.com/CCO1BWw.png)
 
 - Here are the individual elements of the GUI and their correct usage:
	 - **Data File Name**: The name and extension of the CSV file that stores the data collected by the Uber and Lyft APIs. Feel free to change the name to whatever you wish.
	 - **Data File Folder**: The directory path of the data file. This field must have a correct value. If no value exists, you will be prompted with an error message. However, if the value is not correct, the program is currently not able to detect that. By default, the location for this file is the directory that you unzipped. Feel free to change the location of the file to a place of your choosing. When choosing a new location, please use the “Browse” button to select a location. You do not have to worry about creating this file before you start the run. The program will automatically create the file for you if it does not already exist.
	 - **Location File Name**: The name and extension of the CSV file that stores the locations that you want to collect data for. A locations.csv file is provided in the folder that you unzipped by default. If you ever want to edit the file, click on the “Edit ‘locations.csv’” hyperlink to do so. Internally, the Locations File must be the exact same format of the provided locations.csv. If you change the format (column order, column names, etc.) the program will not work. Therefore, it is best to always click this blue hyperlink if you want to change any of the locations.
	 - **Location File Folder**: The directory path of the Locations file. This field must have a correct value. If no value exists, you will be prompted with an error message. However, if the value is not correct, the program is currently not able to detect that. By default, the location of this file is the directory that you unzipped. Feel free to change the location of the file to a place of your choosing. When choosing a new location, please use the “Browse” button to select a new location. You must manually move the Locations file to the selected location before starting the run.
	 - **Selected Locations**: The program looks inside the Locations file and populates this list with the locations in that file. If there is nothing in this list, then either the Locations File Folder field does not contain the correct path to the file or the value in the Location File Name does not contain the correct name and extension of the Locations file on your computer. 
	 - **Run Status**: This text can either display “Not Running” or “Running” depending on if you have started a run or not. As of now, this field does not update if an error has occurred with the run.
	 - **Progress**: When a run has started, you will be updated with the current location that the program is collecting data for. If you do not see any status updates in this area after hitting “Start” or you see the same status update appearing repeatedly, that means an error has occurred with the program.

Warnings and Other Information
------------------------------

 - The program is still restricted by Uber’s 2000 requests per hour limit. However, if 2000 requests have been exceeded within an hour, the program has been designed to not crash. But for best results please try not to exceed 2000 requests per hour. The Progress area outputs information about how many Uber requests have been made during the current hour, so use this information to determine if and when another run should start.
 - Given the 2000 requests per-hour limit, make sure that there is not somebody else running the same version of the program as you during the hour that you are collecting data. However, you may run one Windows and one Mac version simultaneously without any problems.
 - Do NOT open the data file (uber-lyft_result.csv by default) while the data collection is running. This will crash the “query_agent” process. If you wish to see the contents of the file while data collection is running, copy and paste the file and open the copy of the file. Also, make sure that the data file is closed before starting the run.
 - If you do not move the data file to a new location after the end of a run, or change the path of the data file in the Data File Folder field, any new runs in the future will be included at the end of the same data file.
 - To avoid any errors occurring, edit the Locations file by clicking on the blue hyperlink rather than opening the file manually on your system. Clicking the blue hyperlink will open the correct file in Excel for you to make changes to. When you are finished making changes, save the file and close it before starting a run.