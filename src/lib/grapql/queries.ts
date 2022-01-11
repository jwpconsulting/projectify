import { gql } from "@apollo/client/core";

export const Query_User = gql`
    query User {
        user {
            email
        }
    }
`;

export const Mutation_Singup = gql`
    mutation Signup($email: String!, $password: String!) {
        signup(email: $email, password: $password) {
            user {
                email
            }
        }
    }
`;

export const Mutation_EmailConfirmation = gql`
    mutation EmailConfirmation($email: String!, $token: String!) {
        emailConfirmation(email: $email, token: $token) {
            user {
                email
            }
        }
    }
`;

export const Mutation_Login = gql`
    mutation Login($email: String!, $password: String!) {
        login(email: $email, password: $password) {
            user {
                email
            }
        }
    }
`;

export const Mutation_Logout = gql`
    mutation Logout {
        logout {
            user {
                email
            }
        }
    }
`;

export const Query_WorkspacesSideNav = gql`
    query WorkspacesSideNav {
        workspaces {
            uuid
            title
            description
        }
    }
`;

export const Query_TaskPage = gql`
    query TaskPage {
        workspaces {
            uuid
            title
            boards {
                uuid
                title
                sections {
                    uuid
                    title
                    tasks {
                        uuid
                        title
                        description
                        subTasks {
                            title
                            description
                        }
                    }
                }
            }
        }
    }
`;
