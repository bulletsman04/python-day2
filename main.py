from fastapi import FastAPI, HTTPException, Response
import sqlite3
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class AlbumRequest(BaseModel):
    title: str
    artist_id: str

@app.on_event("startup")
async def startup():
    app.db_connection = sqlite3.connect('chinook.db')


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()


@app.get('/tracks')
async def getTracks(page: int = 0, per_page: int = 10):
    app.db_connection.row_factory = sqlite3.Row
    tracks = app.db_connection.execute("SELECT * FROM tracks").fetchall()
    result = tracks[page*per_page:((page+1)*per_page)]
    return result

@app.get('/tracks/composers')
async def getTracksOfComposer(composer_name: str):
    app.db_connection.row_factory = lambda cursor, x: x[0]
    tracks = app.db_connection.execute("SELECT name FROM tracks WHERE Composer = ? ORDER BY name ASC", (composer_name, )).fetchall()
    
    if len(tracks) == 0:
        raise HTTPException(status_code=404, detail={"error":"Not found"})
    
    return tracks

@app.post('/albums')
async def getTracks(req: AlbumRequest):
    app.db_connection.row_factory = lambda cursor, x: x[0]
    artist_exists = app.db_connection.execute("SELECT count() FROM artists WHERE ArtistId = ?", (req.artist_id,)).fetchone() == 1
    
    if artist_exists == False:
        raise HTTPException(status_code=404, detail={"error":"Not found"})
    
    cursor = app.db_connection.execute(
            "INSERT INTO albums (title, ArtistId) VALUES (?,?)", (req.title ,req.artist_id,)
        )
    app.db_connection.commit()
    new_artist_id = cursor.lastrowid
    app.db_connection.row_factory = sqlite3.Row
    artist = app.db_connection.execute(
            """SELECT AlbumId, Title, ArtistId
            FROM albums WHERE AlbumId = ?""",
            (new_artist_id, )).fetchone()
    return JSONResponse(content=dict(artist), status_code=201)



@app.get('/albums/{album_id}')
async def getTracks(album_id: int):
    app.db_connection.row_factory = sqlite3.Row
    album = app.db_connection.execute("SELECT * FROM albums WHERE AlbumId = ?", (album_id ,)).fetchone()
    if album == None:
        raise HTTPException(status_code=404, detail={"error":"Not found"})
    return album

