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

export const Mutation_RequesetPasswordReset = gql`
    mutation RequesetPasswordReset($input: RequestPasswordResetInput!) {
        requestPasswordReset(input: $input) {
            email
        }
    }
`;

export const Mutation_ConfirmPasswordReset = gql`
    mutation ConfirmPasswordReset($input: ConfirmPasswordResetInput!) {
        confirmPasswordReset(input: $input) {
            user {
                email
            }
        }
    }
`;

export const Query_Dashboard = gql`
    query Query_Dashboard {
        workspaces {
            uuid
            title
            boards {
                uuid
                title
                sections {
                    uuid
                    title
                    order
                    tasks {
                        uuid
                        title
                        description
                        order
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

export const Query_DashboardWorkspacesSideNav = gql`
    query DashboardWorkspacesSideNav {
        workspaces {
            uuid
            title
            description
        }
    }
`;

export const Query_DashboardBoardsSideNav = gql`
    query DashboardBoardsSideNav($uuid: ID!) {
        workspace(uuid: $uuid) {
            uuid
            boards {
                uuid
                title
            }
        }
    }
`;

export const Query_DashboardBoard = gql`
    query DashboardBoard($uuid: ID!) {
        workspaceBoard(uuid: $uuid) {
            uuid
            title
            description
            sections {
                order
                uuid
                title
                tasks {
                    order
                    uuid
                    title
                }
            }
        }
    }
`;

export const Subscription_OnWorkspaceBoardChange = gql`
    subscription OnWorkspaceBoardChange($uuid: ID!) {
        onWorkspaceBoardChange(uuid: $uuid) {
            workspaceBoard {
                uuid
                title
                description
                sections {
                    uuid
                    title
                    tasks {
                        uuid
                        title
                    }
                }
            }
        }
    }
`;

export const Query_DashboardTaskDetails = gql`
    query DashboardTaskDetails($uuid: ID!) {
        task(uuid: $uuid) {
            uuid
            title
            description
            subTasks {
                uuid
                title
                description
                done
            }
        }
    }
`;

export const Mutation_AddTask = gql`
    mutation AddTask($input: AddTaskMutationInput!) {
        addTask(input: $input) {
            task {
                uuid
                created
            }
        }
    }
`;

export const Mutation_MoveTask = gql`
    mutation MoveTask($input: MoveTaskInput!) {
        moveTask(input: $input) {
            task {
                uuid
            }
        }
    }
`;

export const Mutation_AddSubTask = gql`
    mutation AddSubTask($input: AddSubTaskInput!) {
        addSubTask(input: $input) {
            subTask {
                uuid
                created
            }
        }
    }
`;

export const Mutation_ChangeSubTaskDone = gql`
    mutation ChangeSubTaskDone($input: ChangeSubTaskDoneInput!) {
        changeSubTaskDone(input: $input) {
            subTask {
                uuid
                created
            }
        }
    }
`;

export const Mutation_DeleteSubTaskMutation = gql`
    mutation DeleteSubTaskMutation($uuid: ID!) {
        deleteSubTask(uuid: $uuid) {
            subTask {
                uuid
            }
        }
    }
`;

export const Mutation_MoveWorkspaceBoardSection = gql`
    mutation MoveWorkspaceBoardSection(
        $input: MoveWorkspaceBoardSectionInput!
    ) {
        moveWorkspaceBoardSection(input: $input) {
            workspaceBoardSection {
                uuid
            }
        }
    }
`;

export const Mutation_AddWorkspaceBoardSection = gql`
    mutation AddWorkspaceBoardSection($input: AddWorkspaceBoardSectionInput!) {
        addWorkspaceBoardSection(input: $input) {
            workspaceBoardSection {
                uuid
                created
                title
                description
                tasks {
                    uuid
                    title
                    description
                }
            }
        }
    }
`;

export const Mutation_AddWorkspaceBoard = gql`
    mutation AddWorkspaceBoard($input: AddWorkspaceBoardInput!) {
        addWorkspaceBoard(input: $input) {
            workspaceBoard {
                uuid
                created
            }
        }
    }
`;
