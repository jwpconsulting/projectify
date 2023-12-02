import { gql } from "@apollo/client/core";

// Mutation
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

export const Mutation_AssignLabel = gql`
    mutation AssignLabel($input: AssignLabelInput!) {
        assignLabel(input: $input) {
            uuid
        }
    }
`;
