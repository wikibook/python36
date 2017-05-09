from datetime import datetime
from google.cloud import datastore

YOUR_PROJECT_ID = "fastpy001"
DS_KIND = "bookmark"
bookmark_list = []

def get_client():
    return datastore.Client(YOUR_PROJECT_ID)

def get_list():
    ds = get_client()
    query = ds.query(kind=DS_KIND, order=['name'])
    query_iter = query.fetch()
    bookmark_list.clear()
    for entity in query_iter:
        #print ("id:" + str(entity.key.id) + " name:" + entity['name'])
        entity['id'] = entity.key.id
        bookmark_list.append(entity)

    return bookmark_list

def update(data, id=None):
    ds = get_client()
    
    if id:
        key = ds.key(DS_KIND, int(id))
    else:
        key = ds.key(DS_KIND)
 
    entity = datastore.Entity(key=key,
        exclude_from_indexes=['date','url'])
    entity.update(data)
    # entity['name'] = 'daum'
    ds.put(entity)
    return entity.key.id

add = update

def delete(id):
    ds = get_client()
    key = ds.key(DS_KIND, int(id))
    ds.delete(key)

if __name__ == '__main__':
    print ("it is bookmark app")
    newbm = {"name":"google", "url":"http://www.google.com", "date": datetime.now() }
    print("insert google url to bookmark")
    id = add(newbm)
    print ("added key's id:" + str(id))
    get_list()
    for en in bookmark_list:
        print ("id:" + str(en['id']) + " name:" + en['name'])
    print("delete google url")
    delete(id)
    get_list()
    for en in bookmark_list:
        print ("id:" + str(en['id']) + " name:" + en['name'])