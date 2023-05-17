

# import the classes for accessing DSS objects from the recipe
import dataiku
# Import the helpers for custom recipes
from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

# Inputs and outputs are defined by roles. In the recipe's I/O tab, the user can associate one
# or more dataset to each input and output role.
# Roles need to be defined in recipe.json, in the inputRoles and outputRoles fields.

# To  retrieve the datasets of an input role named 'input_A' as an array of dataset names:
input_A_names = get_input_names_for_role('input_A_role')
# The dataset objects themselves can then be created like this:
input_A_datasets = [dataiku.Dataset(name) for name in input_A_names]

# For outputs, the process is the same:
output_A_names = get_output_names_for_role('main_output')
output_A_datasets = [dataiku.Dataset(name) for name in output_A_names]


# The configuration consists of the parameters set up by the user in the recipe Settings tab.

# Parameters must be added to the recipe.json file so that DSS can prompt the user for values in
# the Settings tab of the recipe. The field "params" holds a list of all the params for wich the
# user will be prompted for values.

# The configuration is simply a map of parameters, and retrieving the value of one of them is simply:
my_variable = get_recipe_config()['parameter_name']

# For optional parameters, you should provide a default value in case the parameter is not present:
my_variable = get_recipe_config().get('parameter_name', None)

# Note about typing:
# The configuration of the recipe is passed through a JSON object
# As such, INT parameters of the recipe are received in the get_recipe_config() dict as a Python float.
# If you absolutely require a Python int, use int(get_recipe_config()["my_int_param"])


#############################
# Your original recipe
#############################

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd

import tableauserverclient as TSC
import datetime

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# get the project variables
client = dataiku.api_client()
proj = client.get_project(dataiku.default_project_key())
variables = proj.get_variables()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# parameters
username = variables['local']["username"]
password = variables['local']["pw"]
sitename = "nebatesting"
server_url = "https://us-west-2b.online.tableau.com/"
api_version = "3.16"
view_name = "Stocks"
folder = dataiku.Folder("image_folder")
token_name = "mytoken"
token_value = "fh2xdFxyRZKZn5ua6S1agw==:E2SagDYSH6BjRguuv4s93epD6jeRIA9y"


# filter parameter keys and values
filters = ["Company", "Google,Apple", "YEAR(Date)", "2010"]
filter_keys = [filters[i] for i in range(len(filters)) if i%2==0]
filter_values = [filters[i] for i in range(len(filters)) if i%2==1]
filter_key_value_pairs = list(zip(filter_keys, filter_values))


# range_filter = ["range_column", "10,20,1"]
# limits_step = range_filter[1].split(",")
# limits_step = [int(value) for value in limits_step]
# range_filter_values = list(range(limits_step[0], limits_step[1]+limits_step[2], limits_step[2]))
# range_filter_values = [str(value) for value in range_filter_values]
# range_filter_values = [",".join(range_filter_values)]
# final_range_filter = [range_filter[0]] + range_filter_values
# filter_key_value_pairs = filter_key_value_pairs + [tuple(final_range_filter)]

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# # alternative for signing into tableau using personal authentication
tableau_auth = TSC.PersonalAccessTokenAuth(token_name, token_value, site_id=sitename)
# get tableau authentication credentials
server = TSC.Server(server_url)
server.version = api_version
print(server.version)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# ## Download image and data

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# get tableau authentication credentials
tableau_auth = TSC.TableauAuth(username, password, sitename)
# get the tableau server url
server = TSC.Server(server_url)
server.version = api_version

# get the current time to be used as part of file names
current_time = datetime.datetime.now()
current_time = current_time.strftime("%m_%d_%Y_%H_%M_%S")

# download and write csv data to a managed folder
with server.auth.sign_in(tableau_auth):
    for view in TSC.Pager(server.views):
        if view_name == view.name:
            # set the csv data request option
            csv_req_option = TSC.CSVRequestOptions(maxage=1)
            # filter the view on some conditions
            for k, v in filter_key_value_pairs:
                csv_req_option.vf(k, v)
            # create a view image
            server.views.populate_csv(view, csv_req_option)
            #write the image of the view
            filename = view_name + "_" + current_time + ".csv"
            folder.upload_stream(filename, view.csv)


# download and write image to a managed folder
with server.auth.sign_in(tableau_auth):
    for view in TSC.Pager(server.views):
        if view_name == view.name:
            # set the image request option
            image_req_option = TSC.ImageRequestOptions(
                        imageresolution=TSC.ImageRequestOptions.Resolution.High,
                        maxage=1)
            # filter the view on some conditions
            for k, v in filter_key_value_pairs:
                image_req_option.vf(k, v)

            # create a view image
            server.views.populate_image(view, image_req_option)
            #write the image of the view
            filename = view_name + "_" + current_time + ".png"
            folder.upload_stream(filename, view.image)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
view.csv

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# you change the API version using: server.version = new_value
#server.version = api_version

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: MARKDOWN
# - Rest api version and the tableau server version are not the same. It is recommended to use the latest api version for your specif server. The default api version will be used which canb be obtained using server.version,