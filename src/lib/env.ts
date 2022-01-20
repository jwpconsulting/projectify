export default {
    GRAPHQL_ENDPOINT: import.meta.env["VITE_GRAPHQL_ENDPOINT"] as string,
    GRAPHQL_ENDPOINT_BATCH: import.meta.env[
        "VITE_GRAPHQL_ENDPOINT_BATCH"
    ] as string,
};
