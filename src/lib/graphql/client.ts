import { ApolloClient, InMemoryCache } from "@apollo/client/core";

import { from, split } from "@apollo/client/link/core";
import { HttpLink } from "@apollo/client/link/http";
import { BatchHttpLink } from "@apollo/client/link/batch-http";
import { onError } from "@apollo/client/link/error";

import vars from "$lib/env";

const batchLinkEnabled = false;

const httpCommonOpts = {
    uri: vars.GRAPHQL_ENDPOINT,
    credentials: "include",
};

const httpLink = batchLinkEnabled
    ? new BatchHttpLink({
          ...httpCommonOpts,
          batchMax: 10, // No more than 5 operations per batch
          batchInterval: 20, // Wait no more than 20ms after first batched operation
      })
    : new HttpLink(httpCommonOpts);

const errorLink = onError(({ graphQLErrors, networkError }) => {
    if (graphQLErrors)
        graphQLErrors.forEach(({ message, locations, path }) =>
            console.log(
                `[GraphQL error]: Message: ${message}, Location: ${locations}, Path: ${path}`
            )
        );

    if (networkError) console.log(`[Network error]: ${networkError}`);
});

export const client = new ApolloClient({
    link: from([errorLink, httpLink]),
    uri: vars.GRAPHQL_ENDPOINT,
    cache: new InMemoryCache(),
});
