from flask_apscheduler import APScheduler
from concurrent.futures import ThreadPoolExecutor
from browser import search_facebook_marketplace
import os

scheduler = APScheduler()



@scheduler.task('cron', id='check_jobs', minute="*")
def min1():
    with ThreadPoolExecutor(max_workers=1) as executor:
         
        if os.environ['Agent_List_Scanner'] == 'Starter':
            executor.submit(start_marketplace_search_scanner)

        if os.environ['Agent_Page_Scanner'] == 'Starter':
            executor.submit()



def start_marketplace_search_scanner():
    try:
        location = os.environ.get("Search_Location")
        search   = os.environ.get("Search_Query")
        os.environ['Agent_List_Scanner'] = "Running"
        search_facebook_marketplace(location,search)
        os.environ['Agent_List_Scanner'] = "Ready"
    except:
        os.environ['Agent_List_Scanner'] = "Ready"