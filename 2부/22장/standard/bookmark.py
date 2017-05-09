from google.appengine.ext import ndb
import time

bookmark_list = []

#create bookmark model.
class bookmark(ndb.Model):
    date = ndb.DateTimeProperty(auto_now_add=True)
    name = ndb.StringProperty()
    url = ndb.StringProperty()

    @classmethod
    def query_bookmark(cls):
        return cls.query().order(-cls.date) #order by date, descending

def get_list():
    del bookmark_list[:] 
    bms = bookmark.query_bookmark().fetch() #query bookmark

    for bm in bms:
        entity = {}
        entity['name'] = bm.name
        entity['url'] = bm.url
        entity['id'] = bm.key.id()
        #print (entity)
        bookmark_list.append(entity)

    return bookmark_list

def update(data, id=None):

    #bm  bookmark()
    if id:
        bm = ndb.Key('bookmark', id)
    else:
        bm = bookmark() 
        bm.id = int(time.time())

    bm.name = data['name']
    bm.url = data['url']
    bm_key = bm.put()

    return bm_key.id()

add = update

def delete(id):
    del_key = ndb.Key('bookmark', id)
    del_key.delete()
