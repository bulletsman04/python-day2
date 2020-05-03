from fastapi import FastAPI
import sqlite3

app = FastAPI()

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
    tracks = app.db_connection.execute("SELECT name FROM tracks WHERE Composer LIKE ? OR Composer LIKE ?", (f'%{composer_name},%',f'%, {composer_name}%',)).fetchall()
    return tracks


