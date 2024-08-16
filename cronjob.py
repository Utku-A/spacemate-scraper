from flask_apscheduler import APScheduler
from concurrent.futures import ThreadPoolExecutor
from database import get_page_scanner_job_link_data
from browser import search_facebook_marketplace, scennar_page_detail
import os

scheduler = APScheduler()



@scheduler.task('cron', id='check_jobs', minute="*")
def min1():
    with ThreadPoolExecutor(max_workers=1) as executor:
         
        if os.environ['Agent_List_Scanner'] == 'Starter':
            executor.submit(start_marketplace_search_scanner)

        if os.environ['Agent_Page_Scanner'] == 'Starter':
            executor.submit(start_detail_page_scanner)



def start_marketplace_search_scanner():
    try:
        location = os.environ.get("Search_Location")
        search   = os.environ.get("Search_Query")
        os.environ['Agent_List_Scanner'] = "Running"
        search_facebook_marketplace(location,search)
        os.environ['Agent_List_Scanner'] = "Ready"
    except:
        os.environ['Agent_List_Scanner'] = "Ready"



def start_detail_page_scanner():
    try:
        os.environ['Agent_Page_Scanner'] = "Running"
        link_data = get_page_scanner_job_link_data()
        for link in link_data:
            if os.environ['Agent_Page_Scanner'] == "Stoped": break
            scennar_page_detail(link[0])
        os.environ['Agent_Page_Scanner'] = "Ready"
    except:
        os.environ['Agent_Page_Scanner'] = "Ready"
