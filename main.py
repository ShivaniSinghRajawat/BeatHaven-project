from flask import Flask, render_template

app = Flask(__name__)


recently_played = [
    {"id": f"song-{i}", "title": f"Song Title {i}", "artist": f"Artist {i}", "album": f"Album {i}"} 
    for i in range(1, 9)
]

playlists = [
    {"id": f"playlist-{i}", "name": f"Playlist {i}", "song_count": 10} 
    for i in range(1, 9)
]

leaderboard = [
    {"id": "1", "name": "User1", "score": 950},
    {"id": "2", "name": "User2", "score": 880},
    {"id": "3", "name": "User3", "score": 750},
]

@app.route('/templates/home.html')
def hello_world():
    return render_template('home.html'
                        )

@app.route('/templates/base.html')
def ello():
    return render_template('base.html',
                          recently_played=recently_played, 
                           playlists=playlists, 
                           leaderboard=leaderboard)
    
@app.route('/about')
def hello():
    return render_template('about.html')

@app.route('/contact_us')
def hell():
    return render_template('contact us.html')

@app.route('/profile')
def hllo():
    return render_template('profile.html')

@app.route('/login')
def helo():
    return render_template('log in.html')

if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True)

