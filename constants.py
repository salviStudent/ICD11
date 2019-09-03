#
#
#
#

################################################################################
#                                                                              #
#                All of the urls we provide a wrapper for                      #
#                                                                              #
################################################################################

BASE_URL = 'http://id.who.int/icd/'

#Foundation api endpoints
ENTITY_URL = BASE_URL + 'entity/'
ENTITY_ID_URL = ENTITY_URL + '{icd11_code}'
ENTITY_SEARCH_URL = ENTITY_URL + 'search' 

#Linnearization endpoints
#    Endpoints with no release id
LINEAR_URL = BASE_URL + 'release/11/{linear}'
LINEAR_ID_URL = LINEAR_URL + '/{{icd11_code}}'
LINEAR_ID_RESIDUAL_URL = LINEAR_ID_URL + '/{residual}'

#    Endpoints that require a release id
LINEAR_RELEASE_URL = BASE_URL + 'release/11/{release_id}/{linear}'
LINEAR_RELEASE_ID_URL = LINEAR_RELEASE_URL + '/{{icd11_code}}'
LINEAR_RELEASE_RESIDUAL_URL = LINEAR_RELEASE_ID_URL + '/{residual}'
LINEAR_RELEASE_SEARCH = BASE_URL + 'release/11/{release_id}/{linear}/search'
RELEASE_CODEINFO_URL = LINEAR_RELEASE_URL + "/codeinfo/{{icd11_code}}"
################################################################################


################################################################################
#                                                                              #
#  The DataItem class we use for preprocessing. Just a lightweight class that  #
#  allows us to keep going with the download in case something fails           #
################################################################################
#This is now deprecated
#DataItem = namedtuple('DataItem',['id','url','content'])
################################################################################


################################################################################
#                                                                              #
#                         Miscellaneous                                        #
#                                                                              #
################################################################################
TOKEN_ENDPOINT = 'https://icdaccessmanagement.who.int/connect/token'
RATE_LIMIT = 0.5
################################################################################
