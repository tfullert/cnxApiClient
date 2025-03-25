import time
import requests
import hashlib
import base64
import hmac
import pprint
from cnxobjects import cnxDomain, cnxDomainRecord, cnxIPFilter

# =============================================================================
# cnxApiClient: Client for accessing the Constellix DNS API.
#   * see: https://api.dns.constellix.com/v4/docs

class cnxApiClient:
    
    base_url = 'https://api.dns.constellix.com/v4'
    
    def __init__(self, api_key, secret_key, base_url=base_url, per_page='50'):
        
        self.base_url   = base_url
        self.api_key    = api_key
        self.secret_key = secret_key
        self.token      = self.generate_token()
        self.per_page   = per_page
        
    def __str__(self):
        
        return f"{{api_key: {self.api_key}, secret_key: {self.secret_key}}}"
    
    # Decorated functions should return array of results.
    def _paginated(paginated_func):
    
        def func_wrapper(*args, **kwargs):
            
            all_results = []
            
            while True:
                
                # Call paginated function, consolidate results, and save next page
                func_results, next_page_url = paginated_func(*args, **kwargs)
                all_results                 = all_results + func_results
                kwargs['page_url']          = next_page_url
                
                # End while loop and return results when no more pages to acquire
                if next_page_url == None:
                    break
            
            return all_results
        
        return func_wrapper
    
    # Function for generating signature used in token
    def generate_token(self):
        
        epoch_time  = str(round(time.time() * 1000))
        hmac_sha1   = hmac.new(self.secret_key.encode('utf-8'), epoch_time.encode('utf-8'), hashlib.sha1)
        signature   = base64.b64encode(hmac_sha1.digest()).decode('utf-8')
        self.token  = self.api_key + ':' + signature + ':' + epoch_time
        
        return self.token
    
    # Create headers for API call
    def generate_headers(self):
    
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.token
        }
        
        return headers
    
    # Get Version of API and ensure it's available
    def ping(self):
        
        url     = self.base_url + '/ping'
        headers = self.generate_headers()
        data    = {}
        rsp     = requests.request("GET", url, headers=headers, data=data)

        return rsp
    
    # Get a list of the domains for an account
    @_paginated        
    def get_domains(self, page_url=None):

        domain_list = []
        nxt_pg_url  = None
        
        gd_url      = self.base_url + '/domains'
        payload     = {}
        headers     = self.generate_headers()

        if page_url == None:
            gd_url = gd_url + f"?perPage={self.per_page}&page=1"
        else:
            gd_url = page_url
        
        # Process results and get next page for pagination
        rsp     = requests.request("GET", gd_url, headers=headers, data=payload)
        rsp_obj = rsp.json()
        
        if rsp_obj['data']:
            
            nxt_pg_url = rsp_obj['meta']['links']['next']
        
            for domain in rsp_obj['data']:
                domain_list.append(cnxDomain(domain))
            
        return domain_list, nxt_pg_url
    
    # Get details for a specific domain
    def get_domain(self, domain_id):
        
        url     = self.base_url + f"/domains/{domain_id}"
        data    = {}
        headers = self.generate_headers()
        
        rsp     = requests.request("GET", url, headers=headers, data=data)
        
        return cnxDomain(rsp.json()['data'])
    
    # Get the name servers that are configured (in parent zone) for the domain.
    # NOTE: May be different than NS RRset of the domain on Constellix.
    def get_domain_nameservers(self, domain_id):
        
        url     = self.base_url + f"/domains/{domain_id}/nameservers"
        data    = {}
        headers = self.generate_headers()
        
        rsp     = requests.request("GET", url, headers=headers, data=data)
        
        return rsp.json()['data']['nameservers']
    
    # Export the domain as a BIND formatted file (text)
    def get_domain_bind_export(self, domain_id):
        
        url     = self.base_url + f"/domains/{domain_id}/bind"
        data    = {}
        headers = self.generate_headers()
        
        rsp     = requests.request("GET", url, headers=headers, data=data)
        
        return rsp.text
    
    # Get a list of the DNS records in a domain
    @_paginated
    def get_domain_records(self, domain_id, page_url=None):
        
        record_list = []
        nxt_pg_url  = None
        
        gdr_url     = self.base_url + f"/domains/{domain_id}/records"
        data        = {}
        headers     = self.generate_headers()

        if page_url == None:
            gdr_url = gdr_url + f"?perPage={self.per_page}&page=1"
        else:
            gdr_url = page_url
        
        rsp     = requests.request("GET", gdr_url, headers=headers, data=data)
        rsp_obj = rsp.json()
        
        if rsp_obj['data']:
            
            nxt_pg_url = rsp_obj['meta']['links']['next']
        
            for record in rsp_obj['data']:
                record.pop('links')
                record_list.append(cnxDomainRecord(record))
            
        return record_list, nxt_pg_url
    
    # Get the details of a specific record in a domain
    def get_domain_record(self, domain_id, record_id):
        
        url     = self.base_url + f"/domains/{domain_id}/records/{record_id}"
        data    = {}
        headers = self.generate_headers()
        
        rsp     = requests.request("GET", url, headers=headers, data=data)
        
        return cnxDomainRecord(rsp.json()['data'])
    
    # Get a list of the IP Filters that are configured in an account
    @_paginated
    def get_ip_filters(self):
        
        ip_filter_list  = []
        nxt_pg_url      = None
        url             = self.base_url + '/ipfilters'
        data            = {}
        headers         = self.generate_headers()
        
        rsp             = requests.request("GET", url, headers=headers, data=data)
        rsp_obj         = rsp.json()
        
        if rsp_obj['data']:
            
            nxt_pg_url = rsp_obj['meta']['links']['next']
        
            for ip_filter in rsp_obj['data']:
                ip_filter.pop('links')
                ip_filter_list.append(cnxIPFilter(ip_filter))
            
        return ip_filter_list, nxt_pg_url
    
    # Get the details of a specific IP filter in the account
    def get_ip_filter(self, filter_id):
        
        url     = self.base_url + f"/ipfilters/{filter_id}"
        data    = {}
        headers = self.generate_headers()
        
        rsp     = requests.request("GET", url, headers=headers, data=data)
        rsp_obj = rsp.json()
        rsp_obj['data'].pop('links')
        
        return cnxIPFilter(rsp_obj['data'])
   
if __name__ == '__main__':

    # Example program: find all domains that have non-standard DNS records
    # by exporting zones in BIND formatted file and searching for the string
    # 'CONSTELLIX-NONRFC-RECORD' which indicates a non-standard record type.
    
    api_key     = '[TODO: API_KEY]'
    secret_key  = '[TODO: SECRET_KEY]'
    
    # Get the list of domains for the account
    cnxClient   = cnxApiClient(api_key, secret_key, per_page=50)
    domains     = cnxClient.get_domains()
    
    for domain in domains:
        print(f"Processing {domain.name}:")
        file = cnxClient.get_domain_bind_export(domain.id)
        
        #print("FILE:", file)
        for line in file.split("\n"):
            if "CONSTELLIX-NONRFC-RECORD" in line:
                print(line.strip())
    