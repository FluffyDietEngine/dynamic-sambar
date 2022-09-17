from prefect import flow

from IGR_MH.meta_scraper import *
from STORAGE.mongo import *

@flow(name='IGR-MH', version= '0.0.1', description='test2')
def flow_test():
    districts = get_districts()
    for district_name, district_code in districts.get('districts').items():
        sros = get_sros(district_name, district_code)
        insert_data('IGR-MH', 'METADATA', sros)

flow_test()
