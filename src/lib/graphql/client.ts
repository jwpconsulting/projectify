import { ApolloClient, InMemoryCache } from "@apollo/client/core";
import { from } from "@apollo/client/link/core";
import { onError } from "@apollo/client/link/error";
import { HttpLink } from "@apollo/client/link/http";

import vars from "$lib/env";

const httpLink = new HttpLink({
    credentials: "include",
    uri: vars.GRAPHQL_ENDPOINT,
});

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
    link: from([errorLink, httpLink]),
    uri: vars.GRAPHQL_ENDPOINT,
    cache: new InMemoryCache(),
    defaultOptions: {
        query: {
            fetchPolicy: "network-only",
            errorPolicy: "all",
        },
    },
});
