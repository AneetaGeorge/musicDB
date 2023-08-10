import { MongoClient } from "mongodb";

let db;

async function connect(cb)
{
    const client = new MongoClient('mongodb://127.0.0.1:27017');
    await client.connect();

    db = client.db('music_db');
    cb();
}

export {db, connect};