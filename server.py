import firebase_admin
from firebase_admin import db
import flask

app = flask.Flask(__name__)

firebase_admin.initialize_app(options={
    'databaseURL': 'https://albumcollectionapi.firebaseio.com'
})

albumsDB = db.reference('albums')

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/albumsdb/albums', methods=['GET'])
def getAllAlbums():
    albums = albumsDB.get()
    return flask.jsonify(albums)

@app.route('/albumsdb/albums/<albumId>', methods=['GET'])
def getAlbumById(albumId):
    return flask.jsonify(_ensure_album(albumId))

@app.route('/albumsdb/albums/<albumId>', methods=['PUT'])
def modifyAlbumById(albumId):
    _ensure_album(albumId)
    req = flask.request.json
    albumsDB.child(albumId).update(req)
    return flask.jsonify({'success': True})

@app.route('/albumsdb/albums', methods=['POST'])
def createNewAlbum():
    req = flask.request.json
    album = albumsDB.push(req)
    return flask.jsonify({'id': album.key}), 201

@app.route('/albumsdb/albums/<albumId>', methods=['DELETE'])
def deleteAlbum(albumId):
    _ensure_album(albumId)
    albumsDB.child(albumId).delete()
    return flask.jsonify({'success': True})

def _ensure_album(id):
    album = albumsDB.child(id).get()
    if not album:
        flask.abort(404)
    return album

if __name__ == "__main__":
    app.run()
