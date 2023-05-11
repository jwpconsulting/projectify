import { ApolloClient, ApolloLink, InMemoryCache } from "@apollo/client/core";

import { from } from "@apollo/client/link/core";
import { HttpLink } from "@apollo/client/link/http";
import { BatchHttpLink } from "@apollo/client/link/batch-http";
import { onError } from "@apollo/client/link/error";

import vars from "$lib/env";

const batchLinkEnabled = false;

const httpCommonOpts = {
    credentials: "include",
};

const httpLink = batchLinkEnabled
    ? new BatchHttpLink({
          ...httpCommonOpts,
          uri: vars.GRAPHQL_ENDPOINT_BATCH,
          batchMax: 10, // No more than 5 operations per batch
          batchInterval: 20, // Wait no more than 20ms after first batched operation
      })
    : new HttpLink({
          ...httpCommonOpts,
          uri: vars.GRAPHQL_ENDPOINT,
      });

const splitLink: ApolloLink = httpLink;

const errorLink = onError(({ graphQLErrors, networkError }) => {
    if (graphQLErrors) {
        graphQLErrors.forEach(({ message, locations, path }) =>
            console.log(
                "[GraphQL error]: Message:",
                message,
                "Location:",
                locations,
                "Path:",
                path
            )
        );
    }

    if (networkError) {
        console.log("[Network error]:", networkError);
    }
});

export const client = new ApolloClient({
    link: from([errorLink, splitLink]),
    uri: vars.GRAPHQL_ENDPOINT,
    cache: new InMemoryCache(),
    defaultOptions: {
        query: {
            fetchPolicy: "network-only",
            errorPolicy: "all",
        },
    },
});
