# Import packages
from censys.search import CensysCertificates
import csv
import os
import sys

# Set environment variables to access data by Censys API
# Using Python Command Line Arguments
os.environ["CENSYS_API_ID"] = sys.argv[1]
os.environ["CENSYS_API_SECRET"] = sys.argv[2]

# Check API Quota function
def check_quota(obj):
    quota = obj.quota()
    if quota.get("allowance") - quota.get("used") > 0:
        return True
    return False    



# main function to call api and return output file path
def call_api():
    
    c = CensysCertificates()

    #check quota
    if not check_quota(c):
        print("Sorry. You are out of API Quota limits")
        return
    
    # fields required to store in csv
    fields = [
        "parsed.fingerprint_sha256",
        "parsed.validity.start",
        "parsed.validity.end",
    ]

    filename = "out.csv"
    page_no = 1

    # to get all the records from all the pages
    while True:
        out = []
        try:
            #using c.search() method to get all the records, max 100
            #from a particular page with the given fields and query
            for record in c.search(
                "parsed.names:censys.io and tags: trusted",
                fields,
                page=page_no,
                max_records=100
            ):
                out.append(record)
            
            #when all the records have been founded and added to output file
            if len(out) == 0:
                break

            print("*"*20)
            print(f"Adding {len(out)} records from page {page_no}...")
            # Write the above records from a particular page to a csv file
            write_csv(out, filename, fields)
            print(f"Records from page {page_no} has been added to the file {filename}")
            # go to next page
            page_no += 1
        
        # to handle exceptions like for 400 (max results) and 
        # CensysTooManyRequestsException
        except Exception as e:
            # add the remaining records still present in the out and to be \
            # appended to the output file
            print(f"Adding the remaining records...")
            write_csv(out, filename, fields)
            #show the exception
            print(e)
            print(f"The file is partially created at {filename}")
            return

    pwd = os.getcwd()
    print(f"The file is successfully created at {pwd}/{filename}")
    return




# function to write csv    
def write_csv(obj, filename, fields):
    # for appending the new rows to the existing file
    if os.path.exists(filename):
        with open(filename, "a") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writerows(obj)
            csvfile.close()
    # for first new entries
    else:       
        with open(filename, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writeheader()
            writer.writerows(obj)
            csvfile.close()
        
        
if __name__ == '__main__':
    call_api()