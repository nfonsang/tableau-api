
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
import tableauserverclient as TSC
import datetime
import csv


from dataiku.customrecipe import get_input_names_for_role
from dataiku.customrecipe import get_output_names_for_role
from dataiku.customrecipe import get_recipe_config

    
# Read the output of the recipe
output_folder_name = get_output_names_for_role('output_folder')[0]
output_folder = dataiku.Folder(output_folder_name)

# Get parameter values from the UI

credential_parameters = get_recipe_config().get("personal_authentication", {})
username = credential_parameters['tableau_personal_auth_basic']["user"]
password = credential_parameters['tableau_personal_auth_basic']["password"]

server_url = get_recipe_config()["server_url"]
api_version = get_recipe_config()["api_version"]
site_id = get_recipe_config()["site_id"]
workbook_name = get_recipe_config()["workbook_name"]
view_name = get_recipe_config()["view_name"]
clear_folder = get_recipe_config()["clear_folder"]
download_csv = get_recipe_config()["download_csv"]

# get filter parameter values
filter = get_recipe_config().get("filter", {})
range_filter = get_recipe_config().get("range_filter", {})
filter_column = get_recipe_config().get("filter_column", "")

# clear folder before downloading the dashboard(s)
if clear_folder:
    output_folder.clear()

# filter parameter keys and values
filter_keys = list(filter.keys())
filter_values = list(filter.values())
filter_key_value_pairs = list(zip(filter_keys, filter_values))

#filter parameter keys and range values
#range_filter = {"col_1": "10,20,1", "col_2": "4,10,2"}

range_filter_keys = list(range_filter.keys())
range_filter_values = list(range_filter.values())
range_filter_keys_2 = []
for pair in range_filter_values:
    limits_step = pair.split(",")
    limits_step = [int(value) for value in limits_step]
    fil_vals = list(range(limits_step[0], limits_step[1]+limits_step[2], limits_step[2]))
    fil_vals = [str(value) for value in fil_vals]
    fil_vals = ",".join(fil_vals)
    range_filter_keys_2.append(fil_vals)
key_value_pairs = list(zip(range_filter_keys, range_filter_keys_2))

## add the range filter to the other filter
filter_key_value_pairs = filter_key_value_pairs + key_value_pairs


# Authentication
tableau_auth = TSC.TableauAuth(username, password, site_id=site_id)

# set api version
server = TSC.Server(server_url)
server.version = api_version

# set the api_version
## Rest api version and the tableau server version are not the same. 
## It is recommended to use the latest api version for your specific server. 
## If api version is not set, the default api version will be used which canb be obtained using server.version

# get the view id from workbook name and view name
with server.auth.sign_in(tableau_auth):
    workbooks_views = []
    for workbook in TSC.Pager(server.workbooks):
        # first populate views in workbook to access the views
        server.workbooks.populate_views(workbook)
        if workbook.name == workbook_name:
            view_items = [view for view in workbook.views if view]
            workbook_view = [(workbook.name, workbook.id, view_items[i].name, 
                                view_items[i].id) for i in range(len(view_items)) if view_items[i].name==view_name]           
view_id = workbook_view[0][-1]        

current_time = datetime.datetime.now()
current_time = current_time.strftime("%m_%d_%Y_%H_%M_%S")

# download and write image and csv data to a managed folder
with server.auth.sign_in(tableau_auth):
    for view in TSC.Pager(server.views):
        if view_id == view.id:
            # set the csv data request option
            csv_req_option = TSC.CSVRequestOptions(maxage=1)
            # set the csv data request option
            image_req_option = TSC.ImageRequestOptions(
                        imageresolution=TSC.ImageRequestOptions.Resolution.High,
                        maxage=1)
            
            # filter the view on some conditions
            for k, v in filter_key_value_pairs:
                csv_req_option.vf(k, v) # csv
                image_req_option.vf(k, v) # image
                # create a view csv and image
            server.views.populate_csv(view, csv_req_option)
            server.views.populate_image(view, image_req_option)
            
            if filter_column:
                # get the dataframe from the csv
                bytes_ = b''.join(view.csv)
                string = bytes_.decode('utf-8')
                csv_reader = csv.reader(string.split('\n'), delimiter=',', quoting=csv.QUOTE_ALL)
                data = [row for row in csv_reader]
                df = pd.DataFrame(data[1:], columns=data[0])
                df = df.dropna(subset=[filter_column], axis="rows")
                # get unique values of column parameter from dataframe
                col_values = df[filter_column].unique().tolist()
                col_key_values = [(filter_column, i) for i in col_values]

                # create key-value pairs for filtering
                for k_v in col_key_values:
                    filter_key_value_pairs.append(k_v)
                    print("Filter: ", filter_key_value_pairs)                    
                    # set the csv data request option
                    csv_req_option = TSC.CSVRequestOptions(maxage=1)
                    # set the csv data request option
                    image_req_option = TSC.ImageRequestOptions(
                        imageresolution=TSC.ImageRequestOptions.Resolution.High,
                        maxage=1)
                    
                    for k, v in filter_key_value_pairs:
                        csv_req_option.vf(k, v) # csv
                        image_req_option.vf(k, v) # image
                        # create a view csv and image
                    server.views.populate_image(view, image_req_option)

                    #write the csv of the view
                    if download_csv:
                        server.views.populate_csv(view, csv_req_option)
                        filename_csv = view.name + "_" + k_v[1] + "_" + current_time + ".csv"
                        output_folder.upload_stream(filename_csv, view.csv)

                    #write the image of the view
                    filename_img = view.name + "_" + k_v[1] + "_" + current_time + ".png"
                    output_folder.upload_stream(filename_img, view.image)
                    # remove the last col key value pair
                    filter_key_value_pairs.remove(k_v)

            else:
                if download_csv:
                    server.views.populate_csv(view, csv_req_option)
                    filename_csv = view.name + "_" + current_time + ".csv"
                    output_folder.upload_stream(filename_csv, view.csv)

                #write the image of the view
                filename_img = view.name + "_" + current_time + ".png"
                output_folder.upload_stream(filename_img, view.image)
