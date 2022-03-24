import { gql } from "@apollo/client/core";

export const Query_User = gql`
    query User {
        user {
            email
            fullName
            profilePicture
        }
    }
`;

export const Mutation_UpdateProfile = gql`
    mutation UpdateProfile($input: UpdateProfileInput!) {
        updateProfile(input: $input) {
            user {
                email
                fullName
                profilePicture
            }
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
            picture
        }
    }
`;

export const Query_WorkspacesSettingsGeneral = gql`
    query WorkspacesSettingsGeneral($uuid: ID!) {
        workspace(uuid: $uuid) {
            uuid
            title
            description
            picture
        }
    }
`;

export const Mutation_UpdateWorkspace = gql`
    mutation UpdateWorkspace($input: UpdateWorkspaceInput!) {
        updateWorkspace(input: $input) {
            workspace {
                uuid
                modified
                title
                description
            }
        }
    }
`;

export const Query_DashboardBoardsSideNav = gql`
    query DashboardBoardsSideNav($uuid: ID!) {
        workspace(uuid: $uuid) {
            uuid
            labels {
                uuid
                name
                color
            }
            boards {
                uuid
                title
            }
        }
    }
`;

export const Query_WorkspaceLabels = gql`
    query WorkspaceLabels($uuid: ID!) {
        workspace(uuid: $uuid) {
            uuid
            labels {
                uuid
                name
                color
            }
        }
    }
`;

export const Mutation_AddLabelMutation = gql`
    mutation AddLabelMutation($input: AddLabelMutationInput!) {
        addLabel(input: $input) {
            label {
                uuid
            }
        }
    }
`;

export const Mutation_UpdateLabelMutation = gql`
    mutation UpdateLabelMutation($input: UpdateLabelMutationInput!) {
        updateLabel(input: $input) {
            label {
                uuid
            }
        }
    }
`;

export const Mutation_DeleteLabelMutation = gql`
    mutation DeleteLabelMutation($input: DeleteLabelInput!) {
        deleteLabel(input: $input) {
            label {
                uuid
            }
        }
    }
`;

export const Query_WorkspaceTeamMembers = gql`
    query WorkspaceTeamMembers($uuid: ID!) {
        workspace(uuid: $uuid) {
            uuid
            users {
                email
                fullName
                profilePicture
            }
        }
    }
`;

export const Mutation_AddUserToWorkspace = gql`
    mutation AddUserToWorkspace($input: AddUserToWorkspaceInput!) {
        addUserToWorkspace(input: $input) {
            workspace {
                uuid
            }
        }
    }
`;

export const Mutation_RemoveUserFromWorkspace = gql`
    mutation RemoveUserFromWorkspace($input: RemoveUserFromWorkspaceInput!) {
        removeUserFromWorkspace(input: $input) {
            workspace {
                uuid
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
                    labels {
                        uuid
                        name
                        color
                    }
                    assignee {
                        email
                        fullName
                        profilePicture
                    }
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
            assignee {
                email
                fullName
                profilePicture
            }
            subTasks {
                uuid
                title
                description
                done
            }
            workspaceBoardSection {
                uuid
            }
            labels {
                uuid
                name
                color
            }
            chatMessages {
                created
                modified
                uuid
                text
                author {
                    email
                    fullName
                    profilePicture
                }
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

export const Mutation_DeleteTask = gql`
    mutation DeleteTask($input: DeleteTaskInput!) {
        deleteTask(input: $input) {
            task {
                uuid
            }
        }
    }
`;

export const Mutation_UpdateTask = gql`
    mutation UpdateTask($input: UpdateTaskMutationInput!) {
        updateTask(input: $input) {
            task {
                uuid
                modified
                title
                description
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
                title
                description
                done
            }
        }
    }
`;

export const Mutation_ChangeSubTaskDone = gql`
    mutation ChangeSubTaskDone($input: ChangeSubTaskDoneInput!) {
        changeSubTaskDone(input: $input) {
            subTask {
                uuid
                modified
                title
                description
                done
            }
        }
    }
`;

export const Mutation_DeleteSubTaskMutation = gql`
    mutation DeleteSubTaskMutation($input: DeleteSubTaskInput!) {
        deleteSubTask(input: $input) {
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
            }
        }
    }
`;

export const Mutation_UpdateWorkspaceBoardSection = gql`
    mutation UpdateWorkspaceBoardSection(
        $input: UpdateWorkspaceBoardSectionInput!
    ) {
        updateWorkspaceBoardSection(input: $input) {
            workspaceBoardSection {
                uuid
                created
                title
                description
            }
        }
    }
`;

export const Mutation_DeleteWorkspaceBoardSection = gql`
    mutation DeleteWorkspaceBoardSection(
        $input: DeleteWorkspaceBoardSectionInput!
    ) {
        deleteWorkspaceBoardSection(input: $input) {
            workspaceBoardSection {
                uuid
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

export const Mutation_UpdateWorkspaceBoard = gql`
    mutation UpdateWorkspaceBoard($input: UpdateWorkspaceBoardInput!) {
        updateWorkspaceBoard(input: $input) {
            workspaceBoard {
                uuid
                modified
                title
                description
            }
        }
    }
`;

export const Mutation_DeleteWorkspaceBoard = gql`
    mutation DeleteWorkspaceBoard($input: DeleteWorkspaceBoardInput!) {
        deleteWorkspaceBoard(input: $input) {
            workspaceBoard {
                uuid
            }
        }
    }
`;

export const Mutation_ArchiveWorkspaceBoard = gql`
    mutation ArchiveWorkspaceBoard($input: ArchiveWorkspaceBoardInput!) {
        archiveWorkspaceBoard(input: $input) {
            workspaceBoard {
                uuid
            }
        }
    }
`;

export const Query_ArchivedWorkspaceBoards = gql`
    query ArchivedWorkspaceBoards($uuid: ID!) {
        workspace(uuid: $uuid) {
            uuid
            archivedBoards {
                uuid
                title
                archived
            }
        }
    }
`;

export const Mutation_AssignTask = gql`
    mutation AssignTask($input: AssignTaskInput!) {
        assignTask(input: $input) {
            task {
                uuid
            }
        }
    }
`;

export const Mutation_AssignLabel = gql`
    mutation AssignLabel($input: AssignLabelInput!) {
        assignLabel(input: $input) {
            task {
                uuid
            }
        }
    }
`;
