# Description 
This plugin provides an API for sending API calls to Tableau and downloading Tableau dashboards into a folder. The plugin allows users to apply filters to customize the results displayed on the dashboard as needed. 

# How to Set up
When installing the plugin in DSS, you will be prompted to build it's code environment. Note that this plugin requires one of these Python versions:  Python 3.6, Python 3.7 Python 3.8, Python 3.9, Python 3.10, Python 3.11.

# Authentication
This plugin Basic Preset authentication: 
The admin of the instance will Add a preset in the plugin Settings,which will allow users to enter their Tableau server username and password to authenticate.

# How to Use
In your DSS project flow, click on the +Recipe button > click Tableau API > select the plugin component needed and continue until you create the recipe, specify the parameter values needed and run the recipe. 

# Plugin components
This plugin currently has one component.
## Download Tableau Dashboard 
This recipe component has the following parameters.
- Tableau API Personal Authentication: the default value is the Perset Personal Authentication.
- Clear the target folder before downloading the dashboard(s): This parameter provides a checkbox and the default is unchecked, meaning that downloaded dashboards will be appended to the content of the output folder. If checked, the output folder will be cleared before the dashboard is downloaded.
- Download the CSV data used to create the dashboard. This parameter provides a checkbox and the default is unchecked, meaning that the CSV that is used to generate the dashboard will not be downloaded. If checked, the CSV that is used to generate the dashboard will be downloaded into the output folder.
- Tableau Server Base URL: This allows users to enter their Tableau Server base URL with no subpath such as http://us-west-2b.online.tableau.com.
- Tableau REST API Version: This allows users to enter the REST API version that matches with their Tableau Server version. For example 3.19.
- Tableau Site ID: This is the Tableau site ID in the Server URL. For example, the site ID in the Tableau Server URL, tableau_server_url/#/site/site_id/views. 
- Workbook Name: This is the name of the workbook. For example, the workbook_name in Tableau Server URL, tableau_server_url/#/site/site_id/workbook_name/view_name.
- Filter (optional): This allows user to pass in filters as key value pairs where the keys representing column names and their corresponding values. Multiple values can be entered, separated by commas with no spaces. For example: Amazon,Apple could be the values of the key, Company. 
- Range filter (optional): This parameter allows users to specify the numerical filter range and the step value for incrementing the values in the range. For example, the filter range values and step could be specified as 2011,2014,1, which means, start from 2011 up to 2014. The recipe generates all the values in the range using the step value. Since the step is 1, the range values will be 2011,2012,2013,2014. If the step value was 2, the range values will be 2011,2013.
- Column (optional): This is the column whose unique values will be used to partition the data after the filters have been applied. Specifying this column means you want the data to be partitioned and you want a dashboard to be generated from each partition.
# License
This plugin is distributed under the [Apache License version 2.0.](https://github.com/nfonsang/tableau-api/blob/main/LICENSE)
