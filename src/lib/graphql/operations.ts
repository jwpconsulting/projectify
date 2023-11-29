import { gql } from "@apollo/client/core";

// Mutation
export const Mutation_UpdateWorkspaceUser = gql`
    mutation UpdateWorkspaceUser($input: UpdateWorkspaceUserInput!) {
        updateWorkspaceUser(input: $input) {
            email
        }
    }
`;

export const Mutation_UpdateProfile = gql`
    mutation UpdateProfile($input: UpdateProfileInput!) {
        updateProfile(input: $input) {
            email
            fullName
            profilePicture
        }
    }
`;

export const Mutation_Signup = gql`
    mutation Signup($input: SignupInput!) {
        signup(input: $input) {
            email
        }
    }
`;

export const Mutation_EmailConfirmation = gql`
    mutation EmailConfirmation($input: EmailConfirmationInput!) {
        emailConfirmation(input: $input) {
            email
        }
    }
`;

export const Mutation_Login = gql`
    mutation Login($input: LoginInput!) {
        login(input: $input) {
            email
        }
    }
`;

export const Mutation_Logout = gql`
    mutation Logout {
        logout {
            email
        }
    }
`;

export const Mutation_RequesetPasswordReset = gql`
    mutation RequesetPasswordReset($input: RequestPasswordResetInput!) {
        requestPasswordReset(input: $input)
    }
`;

export const Mutation_ConfirmPasswordReset = gql`
    mutation ConfirmPasswordReset($input: ConfirmPasswordResetInput!) {
        confirmPasswordReset(input: $input) {
            email
        }
    }
`;

export const Mutation_AddLabelMutation = gql`
    mutation AddLabelMutation($input: AddLabelInput!) {
        addLabel(input: $input) {
            uuid
        }
    }
`;

export const Mutation_UpdateLabelMutation = gql`
    mutation UpdateLabelMutation($input: UpdateLabelInput!) {
        updateLabel(input: $input) {
            uuid
        }
    }
`;

export const Mutation_DeleteLabelMutation = gql`
    mutation DeleteLabelMutation($input: DeleteLabelInput!) {
        deleteLabel(input: $input) {
            uuid
        }
    }
`;

export const Mutation_RemoveUserFromWorkspace = gql`
    mutation RemoveUserFromWorkspace($input: RemoveUserFromWorkspaceInput!) {
        removeUserFromWorkspace(input: $input) {
            uuid
        }
    }
`;

export const Mutation_DeleteTask = gql`
    mutation DeleteTask($input: DeleteTaskInput!) {
        deleteTask(input: $input) {
            uuid
        }
    }
`;

export const Mutation_MoveTaskAfter = gql`
    mutation MoveTaskAfter($input: MoveTaskAfterInput!) {
        moveTaskAfter(input: $input) {
            uuid
        }
    }
`;

export const Mutation_MoveWorkspaceBoardSection = gql`
    mutation MoveWorkspaceBoardSection(
        $input: MoveWorkspaceBoardSectionInput!
    ) {
        moveWorkspaceBoardSection(input: $input) {
            uuid
        }
    }
`;

export const Mutation_AddWorkspaceBoardSection = gql`
    mutation AddWorkspaceBoardSection($input: AddWorkspaceBoardSectionInput!) {
        addWorkspaceBoardSection(input: $input) {
            uuid
            created
            title
            description
        }
    }
`;

export const Mutation_UpdateWorkspaceBoardSection = gql`
    mutation UpdateWorkspaceBoardSection(
        $input: UpdateWorkspaceBoardSectionInput!
    ) {
        updateWorkspaceBoardSection(input: $input) {
            uuid
            created
            title
            description
        }
    }
`;

export const Mutation_DeleteWorkspaceBoardSection = gql`
    mutation DeleteWorkspaceBoardSection(
        $input: DeleteWorkspaceBoardSectionInput!
    ) {
        deleteWorkspaceBoardSection(input: $input) {
            uuid
        }
    }
`;

export const Mutation_AddWorkspaceBoard = gql`
    mutation AddWorkspaceBoard($input: AddWorkspaceBoardInput!) {
        addWorkspaceBoard(input: $input) {
            uuid
            created
        }
    }
`;

export const Mutation_UpdateWorkspaceBoard = gql`
    mutation UpdateWorkspaceBoard($input: UpdateWorkspaceBoardInput!) {
        updateWorkspaceBoard(input: $input) {
            uuid
            modified
            title
            description
        }
    }
`;

export const Mutation_DeleteWorkspaceBoard = gql`
    mutation DeleteWorkspaceBoard($input: DeleteWorkspaceBoardInput!) {
        deleteWorkspaceBoard(input: $input) {
            uuid
        }
    }
`;

export const Mutation_ArchiveWorkspaceBoard = gql`
    mutation ArchiveWorkspaceBoard($input: ArchiveWorkspaceBoardInput!) {
        archiveWorkspaceBoard(input: $input) {
            uuid
        }
    }
`;

export const Mutation_AssignTask = gql`
    mutation AssignTask($input: AssignTaskInput!) {
        assignTask(input: $input) {
            uuid
        }
    }
`;

export const Mutation_AssignLabel = gql`
    mutation AssignLabel($input: AssignLabelInput!) {
        assignLabel(input: $input) {
            uuid
        }
    }
`;

export const Mutation_AddChatMessage = gql`
    mutation AddChatMessage($input: AddChatMessageInput!) {
        addChatMessage(input: $input) {
            uuid
        }
    }
`;
