import { GraphQLClient } from "graphql-request";
import vars from "$lib/env";

export const client = new GraphQLClient(vars.GRAPHQL_ENDPOINT, {
    credentials: "include",
    mode: "cors",
});
