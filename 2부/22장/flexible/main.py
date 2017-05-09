# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
from flask import redirect, render_template, request, url_for, Flask, current_app
from bookmark import get_list, add, delete

app = Flask(__name__)
app.debug = True     #debug mode

@app.route('/')
def bookmarklist():
    """Return a friendly HTTP greeting."""
    bookmarks = get_list()
    return render_template(
        "home.html",
        bookmarks=bookmarks)

@app.route('/addbookmark', methods=['POST'])
def addbookmark():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        id = add(data)
        print ("added id is " + str(id))

        return redirect("/")

    return "error"

@app.route('/delbookmark', methods=['POST'])
def delbookmark():
    if request.method == 'POST':
        data = request.form.getlist('check')
        for id in data:
            delete(int(id))
            print ("deleted id is " + str(id))

        return redirect("/")

    return "error"
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
# [END app]
