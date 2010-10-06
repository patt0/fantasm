""" Unit testing fixtures """
import os
import unittest
import google.appengine.api.labs.taskqueue.taskqueue_stub as taskqueue_stub
import google.appengine.api.datastore_file_stub as datastore_file_stub
import google.appengine.api.apiproxy_stub_map as apiproxy_stub_map
import google.appengine.api.urlfetch_stub as urlfetch_stub
import google.appengine.api.memcache.memcache_stub as memcache_stub
import google.appengine.api.capabilities.capability_stub as capability_stub

# pylint: disable-msg=C0111
# - docstrings not reqd in unit tests

os.environ['APPLICATION_ID'] = 'fantasm'

class AppEngineTestCase(unittest.TestCase):
    
    def setUp(self):
        super(AppEngineTestCase, self).setUp()

        # save the apiproxy
        self.__origApiproxy = apiproxy_stub_map.apiproxy

        # make a new one
        apiproxy_stub_map.apiproxy = \
            apiproxy_stub_map.APIProxyStubMap()

        self.__taskqueue = taskqueue_stub.TaskQueueServiceStub(root_path='.')
        apiproxy_stub_map.apiproxy.RegisterStub('taskqueue', self.__taskqueue)
        
        self.__urlfetch = urlfetch_stub.URLFetchServiceStub()
        apiproxy_stub_map.apiproxy.RegisterStub('urlfetch', self.__urlfetch)
        
        self.__memcache = memcache_stub.MemcacheServiceStub()
        apiproxy_stub_map.apiproxy.RegisterStub('memcache', self.__memcache)
        
        self.__datastore = datastore_file_stub.DatastoreFileStub('fantasm', '/dev/null', '/dev/null', 
                                                                 require_indexes=True)
        apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', self.__datastore)
        
        self.__capabilities = capability_stub.CapabilityServiceStub()
        apiproxy_stub_map.apiproxy.RegisterStub('capability_service', self.__capabilities)
        
    def tearDown(self):
        super(AppEngineTestCase, self).tearDown()

        # restore the apiproxy
        apiproxy_stub_map.apiproxy = self.__origApiproxy