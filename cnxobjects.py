# ===========================================================================
# cnxObject: Base object that all Constellix objects inherit from.  Creating 
# Constellix objects involves just saving the data structure returned from 
# the API (possibly with some minor modifications like removing 'links') and 
# then creating getters for the values you want to access.  The underlying 
# API data structure is available via the 'api_obj' getter.  The 'header' is 
# an array that can be used to define the data structure properties that
# you want printed/returned from the 'display' or '__str__' methods. 

class cnxObject:
    
    # Initialize the object:
    # * api_obj [dict]  : Object returned from an API call.
    # * header [list]   : List of attributes that will be printed.
    def __init__(self, api_obj, header):    
        self._api_obj   = api_obj
        self._header    = header
    
    # String representation of a cnxObject.
    def __str__(self):
        return ''

    # Get the stored API response.
    @property
    def api_obj(self):
        return self._api_obj
    
    # Get the list of attributes to be returned by 'display' method.
    @property
    def header(self):
        return ','.join(map(str, self._header))

    # Set the header to the provided List.
    @header.setter
    def header(self, header):
        self._header = header
        
    # Display the objects based on the attributes defined by _header.
    # NOTE: A value in _header must have a getter/property method defined.
    def display(self):
        return ','.join(map(str, [getattr(self, head) for head in self._header]))
        

# =============================================================================
# cnxDomain: A Constellix domain object.

class cnxDomain(cnxObject):
    
    def __init__(self, domain_obj):
        header = [
            'id',           # id
            'name',         # name
            'status',       # status
            'enabled',      # enabled
            'geoip',        # geoip
            'gtd',          # gtd
            'ns',           # nameservers
            'vanity_ns',    # vanityNameserver
            'note',         # note
        ]
        
        cnxObject.__init__(self, domain_obj, header)
        
    @property
    def id(self):
        return self._api_obj['id']
        
    @property
    def name(self):
        return self._api_obj['name']
        
    @property
    def status(self):
        return self._api_obj['status']
    
    @property
    def enabled(self):
        return self._api_obj['enabled']
        
    @property
    def geoip(self):
        return self._api_obj['geoip']
        
    @property
    def gtd(self):
        return self._api_obj['gtd']
        
    @property
    def ns(self):
        return self._api_obj['nameservers']
        
    @property
    def vanity_ns(self):
        return self._api_obj['vanityNameserver']
        
    @property
    def note(self):
        return self._api_obj['note']
        
# =============================================================================
# cnxDomainRecord: A Constellix DNS record object.

class cnxDomainRecord(cnxObject):

    def __init__(self, domain_record_obj):
        header = [
            'id',       # id
            'name',     # name
            'type',     # type
            'ttl',      # ttl
            'ipfilter', # ipfilter
        ]
        
        cnxObject.__init__(self, domain_record_obj, header)
    
    @property
    def id(self):
        return self._api_obj['id']
    
    @property
    def name(self):
        return self._api_obj['name']
        
    @property
    def type(self):
        return self._api_obj['type']
        
    @property
    def ttl(self):
        return self._api_obj['ttl']
       
    @property
    def mode(self):
        return self._api_obj['mode']
    
    @property
    def region(self):
        return self._api_obj['region']
    
    @property
    def ipfilter(self):
        return self._api_obj['ipfilter']
        
    @property
    def geo_failover(self):
        return self._api_obj['geoFailover']
        
    @property
    def geo_proximity(self):
        return self._api_obj['geoproximity']
        
    @property
    def value(self):
        return self._api_obj['value']
        
    @property
    def last_values(self):
        return self._api_obj['lastValues']
    
    @property
    def failover(self):
        return self._api_obj['failover']

# =============================================================================
# cnxIPFilter: A Constellix IP Filter object.
class cnxIPFilter(cnxObject):
    
    def __init__(self, ip_filter_obj):
        header = [
            'id',   # id
            'name', # name
            'asn',  # asn
        ]
        
        cnxObject.__init__(self, ip_filter_obj, header)
        
    @property
    def id(self):
        return self._api_obj['id']
    
    @property
    def name(self):
        return self._api_obj['name']
        
    @property
    def rules_limit(self):
        return self._api_obj['rulesLimit']
        
    @property
    def continents(self):
        return self._api_obj['continents']
        
    @property
    def countrires(self):
        return self._api_obj['countries']
        
    @property
    def asn(self):
        return self._api_obj['asn']
        
    @property
    def ipv4(self):
        return self._api_obj['ipv4']
        
    @property
    def ipv6(self):
        return self._api_obj['ipv6']
    
    @property
    def regions(self):
        return self._api_obj['regions']

# =============================================================================
    
