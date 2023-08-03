export default {
    GRAPHQL_ENDPOINT: import.meta.env.VITE_GRAPHQL_ENDPOINT as string,
    // TODO remove me Justus 2023-08-03
    GRAPHQL_ENDPOINT_BATCH: import.meta.env
        .VITE_GRAPHQL_ENDPOINT_BATCH as string,
    // TODO remove me Justus 2023-08-03
    GRAPHQL_ENDPOINT_SUBSCRIPTIONS: import.meta.env
        .VITE_GRAPHQL_ENDPOINT_SUBSCRIPTIONS as string,

    WS_ENDPOINT: import.meta.env.VITE_WS_ENDPOINT as string,
    API_ENDPOINT: import.meta.env.VITE_API_ENDPOINT as string,
};
