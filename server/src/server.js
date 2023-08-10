import express from 'express';
import {db, connect} from './db.js';

const app = express();
app.use(express.json()); //Parse json req body

app.post('/hello', (req, res)=>{
    res.send(`Hello ${req.body.name}!`);
});

// Get all artists -- working
app.get('/api/artists', async (req, res) => {

    const artists = await db.collection('artists').find().toArray();;

    if (artists)
    {
        res.json(artists);
    }

    else
    {
        res.sendStatus(404);
    }
});

// Get artist details for one artist -- working
app.get('/api/artist/:name', async (req, res) => {
    const { name } = req.params;

    const artist = await db.collection('artists').findOne({name});
    console.log(artist)
    if (artist)
    {
        res.json(artist);
    }
    else
    {
        res.sendStatus(404);
    }
});

// Get all albums of one artist
app.get('/api/artist/:name/albums', async (req, res) => {
    const { name } = req.params;

    // const albums = await db.collection('release-groups').find({'artist-credit': { $elemMatch : {'name' : name}}});
    const albums = await db.collection('release-groups').find({'artist-credit.name' : 'BTS'}).toArray();

    if (albums)
    {
        res.json(albums);
    }
    else
    {
        res.sendStatus(404);
    }
});

connect( () => {
    app.listen(8001, ()=>{
        console.log('Server is listening on port 8001');
});
});
