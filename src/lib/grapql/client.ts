import { ApolloClient, InMemoryCache } from "@apollo/client/core";
import { BatchHttpLink } from "@apollo/client/link/batch-http";
import vars from "$lib/env";

const batchLinkEnabled = false;

const batchLink = new BatchHttpLink({
    uri: vars.GRAPHQL_ENDPOINT,
    batchMax: 10, // No more than 5 operations per batch
    batchInterval: 20, // Wait no more than 20ms after first batched operation
});

export const client = new ApolloClient({
    link: batchLinkEnabled ? batchLink : null,
    uri: vars.GRAPHQL_ENDPOINT,
    cache: new InMemoryCache(),
    credentials: "include",
});
