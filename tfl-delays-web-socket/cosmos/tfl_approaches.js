import { CosmosClient } from '@azure/cosmos';
import config from './config.js';
import { create } from './database_context.js';

async function main() {
    const { endpoint, key, databaseId, containerId } = config;

    const client = new CosmosClient({ endpoint, key });
    
    const database = client.database(databaseId);
    const container = database.container(containerId);
    
    // Make sure Tasks database is already setup. If not, create it.
    await create(client, databaseId, containerId);
}

main();