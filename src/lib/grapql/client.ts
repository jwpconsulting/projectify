import { ApolloClient, InMemoryCache } from "@apollo/client/core";
import vars from "$lib/env";

export const client = new ApolloClient({
    uri: vars.GRAPHQL_ENDPOINT,
    cache: new InMemoryCache(),
    credentials: "include",
});
