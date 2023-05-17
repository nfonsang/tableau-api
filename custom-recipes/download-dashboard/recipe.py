
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
import tableauserverclient as TSC
import datetime

from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

    
# Read the output of the recipe
output_folder_name = get_output_names_for_role('output_folder')[0]
output_folder = dataiku.Folder(output_folder_name)

# Get parameter values from the UI

use_token = get_recipe_config()["useToken"]
username = get_recipe_config()["username"]
password = get_recipe_config()["password"]
token_name = get_recipe_config().get("token_name", None)
token_value = get_recipe_config().get("token_value", None)
server_url = get_recipe_config()["server_url"]
api_version = get_recipe_config()["api_version"]
site_id = get_recipe_config()["site_id"]
view_id = get_recipe_config()["view_id"]
filter = get_recipe_config().get("filter", {})

# filter parameter keys and values
filter_keys = list(filter.keys())
filter_values = list(filter.values())
filter_key_value_pairs = list(zip(filter_keys, filter_values))

# range_filter = ["range_column", "10,20,1"]
# limits_step = range_filter[1].split(",")
# limits_step = [int(value) for value in limits_step]
# range_filter_values = list(range(limits_step[0], limits_step[1]+limits_step[2], limits_step[2]))
# range_filter_values = [str(value) for value in range_filter_values]
# range_filter_values = [",".join(range_filter_values)]
# final_range_filter = [range_filter[0]] + range_filter_values
# filter_key_value_pairs = filter_key_value_pairs + [tuple(final_range_filter)]

# Authentication
#if use_token:
 #   tableau_auth = TSC.PersonalAccessTokenAuth(token_name, token_value, site_id=site_id)
#else:
   # tableau_auth = TSC.TableauAuth(username, password, site_id)

#tableau_auth = TSC.TableauAuth(username, password, site_id)

# set the api_version
## Rest api version and the tableau server version are not the same. 
## It is recommended to use the latest api version for your specific server. 
## If api version is not set, the default api version will be used which canb be obtained using server.version

# get tableau authentication credentials
tableau_auth = TSC.TableauAuth(username, password, site_id)
# get the tableau server url
server = TSC.Server(server_url)
server.version = api_version

# get the current time to be used as part of file names
current_time = datetime.datetime.now()
current_time = current_time.strftime("%m_%d_%Y_%H_%M_%S")


# download and write csv data to a managed folder
with server.auth.sign_in(tableau_auth):
    for view in TSC.Pager(server.views):
        if view_id == view.id:
            print("ok")






















