"""
Actual implementation of the API wrapper

We currently cover the following endpoints for foundation:

/icd/entity

/icd/entity/{id}

/icd/entity/search

We currently cover the following endpoints for Linearization:

/icd/release/11/{linearizationname}

/icd/release/11/{releaseId}/{linearizationname}

/icd/release/11/{linearizationname}/{id}

/icd/release/11/{linearizationname}/{id}/{residual}

/icd/release/11/{releaseId}/{linearizationname}/{id}

/icd/release/11/{releaseId}/{linearizationname}/{id}/{residual}

/icd/release/11/{releaseId}/{linearizationname}/search

"""
#std library imports: Pool object from multiprocessing module

from multiprocessing import Pool

#outside dependencies: Session object from the requests module
from requests import Session

#in house code: constants, utility functions and error files.
from . import constants as consts
from . import errors as ers
from .utils import update_token, check_for_string, check_for_bool




def foundation_data(icd11_code):
    """Retrieve data for a single ICD11 code from Foundation"""
    return extract_id_data(icd11_code, consts.ENTITY_ID_URL)

def foundation_search(query, subtrees_filter=None, flexi_search=False,
                               chapter_filter = None, flat_results = True,
                               props_to_search = None, release_id = None):
    """
Search through the foundation api


"""
    return extract_search_data(url=consts.ENTITY_SEARCH_URL, query=query,
                               subtrees_filter=subtrees_filter, flexi_search=flexi_search,
                               chapter_filter=chapter_filter, flat_results=flat_results,
                               props_to_search=props_to_search, release_id=release_id)


def batch_icd11_data(ids, thread_count=1):
    """Return data for a list of icd11 codes"""
    if not isinstance(thread_count, int):
        #thread_count needs to be an integer for the pool object
        #to work. This throws a ValueError to signify that the
        #given thread count is not the correct type
        raise ValueError('thread_count needs to be of type int, you provided: ',
                         type(thread_count))
    if thread_count <= 0:
        #thread_count needs to be greater than 0 to do any actual
        #work. Raises a ValueError 
        raise ValueError('You can not specify', thread_count,
                         'threads as thread_count')
    if thread_count > 1:
        pool = Pool(thread_count)
        results = pool.map(icd11_data,ids)
        return list(results)
    return list(map(icd11_data,ids))


def linearization_data(icd11_code,linear='mms', residual=None):
    """"""
    if residual:
        if not isinstance(residual, str):
            raise ValueError('Expected residual code in string format you passed:',
                         type(residual))
        url = consts.LINEAR_ID_RESIDUAL_URL.format(linear=linear,residual=residual)
        return extract_id_data(icd_code, url)
    
    url = consts.LINEAR_ID_URL.format(linear=linear)
    return extract_id_data(icd11_code, url)
    

def release_data(icd11_code,release_id='2019-04', linear='mms',residual=None):
    """Return data for a single ICD11 code from a specified linearization and release"""
    if residual:
        check_for_string(residual,'residual')
        url = consts.LINEAR_ID_RESIDUAL_URL.format(linear=linear,residual=residual)
        return extract_id_data(icd11_code, url)
    check_for_string(release_id, 'release_id')
    check_for_string(linear, 'linear')
    url = consts.LINEAR_RELEASE_ID_URL.format(release_id=release_id, linear=linear)
    return extract_id_data(icd11_code, url)

def release_code_info(icd11_code,release_id='2019-04', linear='mms'):
    check_for_string(release_id, 'release_id')
    check_for_string(linear, 'linear')
    url = consts.RELEASE_CODEINFO_URL.format(release_id=release_id, linear=linear)
    return extract_id_data(icd11_code, url)

def linearization_search(query, release_id='2019-04', linear='mms',
                               subtrees_filter=None, flexi_search=False,
                               chapter_filter = None, flat_results = True,
                               props_to_search = None,keyword_res =False):
    check_for_string(query,'query')
    check_for_string(release_id,'release_id')
    check_for_string(linear, 'linear')
    url = consts.LINEAR_RELEASE_SEARCH.format(release_id=release_id, linear = linear)
    return extract_search_data(url=url,query=query, subtrees_filter=subtrees_filter,
                               flexi_search=flexi_search, chapter_filter=chapter_filter,
                               flat_results=flat_results, props_to_search=props_to_search,
                               release_id = None, keyword_res=keyword_res)


def extract_id_data(icd11_code,url):
    """End point for api calls that have an icd11 code at the end"""
    if not isinstance(icd11_code, str):
        raise ValueError('Expected icd11 code in string format you passed: ' +
                         type(icd11_code).__name__)
    response = SESH.get(url.format(icd11_code=icd11_code))
    if response.status_code == 404:
        raise ers.ICD11CodeError('Could not find icd11 code: ' + icd11_code)
    elif response.status_code == 401:
        raise ers.AuthorizationError('You are not authorized to access that resource. Check that your config file is correct.')
    return response.json()

def extract_search_data(url, query, subtrees_filter=None, flexi_search=False,
                         chapter_filter = None, flat_results = True,
                         props_to_search = None, release_id = None, keyword_res = False):
    new_url = url + '?q=' + query
    if subtrees_filter is not None:
        check_for_string(subtrees_filter,'subtrees_filter')
        new_url = new_url + '&subtreesFilter=' + subtrees_filter
    if chapter_filter is not None:
        check_for_string(subtrees_filter,'chapter_filter')
        new_url = new_url + '&chapterFilter=' + chapter_filter
    if props_to_search is not None:
        check_for_string(props_to_search, 'props_to_search')
        new_url =  new_url + 'propertiesToBeSearched=' + props_to_search
    #handle all the fields that should be boolean values
    check_for_bool(flexi_search, 'flexi_search')
    check_for_bool(flat_results, 'flat_results')
    check_for_bool(keyword_res, 'keyword_res')
    if flexi_search:
        new_url =  new_url + '&useFlexisearch=' + 'true'
    else:
        new_url =  new_url + '&useFlexisearch=' + 'false'
    if flat_results:
        new_url =  new_url + '&flatResults=' + 'true'
    else:
        new_url =  new_url + '&flatResults=' + 'false'
    if release_id is not None:
        check_for_string(release_id,'release_id')
        new_url = new_url + '&releaseId=' + release_id
    if keyword_res:
        new_url =  new_url + '&includeKeywordResult=' + 'true'
    response = SESH.get(new_url)
    if response.status_code == 404:
        raise ValueError('Could not execute query: ' + new_url)
    elif response.status_code == 401:
        raise ers.AuthorizationError('You are not authorized to access that resource. Check that your config file is correct.')
    return response.json()


  
#initializes the session object each of the api calls use and sets
#the correct values for it
SESH = Session()
update_token(SESH)
