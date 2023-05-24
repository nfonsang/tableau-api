# Description 
This plugin provides an API for sending API calls to Tableau and downloading Tableau dashboards into a folder. The plugin allows users to apply filters to customize the results displayed on the dashboard as needed. 

# How to Set up
When installing the plugin into DSS, you will be prompted to build it's code environment. Note that this plugin requires one of these Python versions:  Python 3.6, Python 3.7 Python 3.8, Python 3.9, Python 3.10, Python 3.11.


# Authentication
This plugin supports two authentication options: 

	- Login authentication: usernname and password required
	- Token authentication: token name and token value required

# How to Use
	- In your DSS project flow, select Recipe > Tableau API
	- Select the Authentication Type 
	- Enter the filter information as key value pairs
	- Enter column name for use cases where filter values are the unique values of a column
	- Select output folder where downloaded view content (such as a dashboard image) will be written
	
# License
This plugin is distributed under the [Apache License version 2.0.](https://github.com/nfonsang/tableau-api/blob/main/LICENSE)
	
