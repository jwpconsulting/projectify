import { gql } from "@apollo/client/core";

export const Query_User = gql`
    query User {
        user {
            email
        }
    }
`;
