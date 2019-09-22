import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'earc2.settings')
import django
django.setup()
import datetime

import xlrd

from django.conf import settings
from django.contrib.auth.models import User
from manage_members.models import Member

FILENAME = os.path.join(settings.BASE_DIR, '../database/earc_membership_list.xlsx')

def import_file():
    wb = xlrd.open_workbook(FILENAME)
    sheet = wb.sheet_by_index(0)
    
    for row_num in range(sheet.nrows):
        row_values = sheet.row_values(row_num)
        row_types = sheet.row_types(row_num)
        if row_values[1] == "KH6WG":
            for i in range(len(row_values)):
                if row_types[i] == 3:
                    row_values[i] = xlrd.xldate.xldate_as_datetime(row_values[i], 0)
            print(row_values)
            break



if __name__ == '__main__':
    import_file()
