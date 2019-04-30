from flask import Flask
from flask import request
from flask import jsonify

albumsDB=[
 {
   'id':'101',
   'artist':'LCD SoundSystem',
   'album_name':'Sound of Silver'
 },
 {
   'id':'102',
   'artist':'The Black Keys',
   'album_name':'The Big Come Up'
 }
]

app = Flask(__name__)
@app.route("/")
def hello():
    return "Hello World!"

@app.route('/albumsdb/albums', methods=['GET'])
def getAllAlbums():
    return jsonify({'albums':albumsDB})

@app.route('/albumsdb/albums/<albumId>', methods=['GET'])
def getAlbumById(albumId):
    album = [ alb for alb in albumsDB if (alb['id'] == albumId) ]
    return jsonify({'album':album})

@app.route('/albumsdb/albums/<albumId>', methods=['PUT'])
def modifyAlbumById(albumId):
    album = [ alb for alb in albumsDB if (alb['id'] == albumId) ]
    if 'album_name' in request.json:
        album[0]['album_name'] = request.json['album_name']
    if 'artist' in request.json:
        album[0]['artist'] = request.json['artist']
    return jsonify({'album':album[0]})

@app.route('/albumsdb/albums', methods=['POST'])
def createNewAlbum():
    newAlb = {
      'id':request.json['id'],
      'album_name': request.json['album_name'],
      'artist': request.json['artist']
    }
    albumsDB.append(newAlb)
    return jsonify(newAlb)

if __name__ == "__main__":
    app.run()
