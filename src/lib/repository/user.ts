import vars from "$lib/env";
import type { User } from "$lib/types/user";
import { getWithCredentialsJson } from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import { uploadImage } from "$lib/utils/file";

// Create
// Read
export async function getUser(
    repositoryContext?: RepositoryContext
): Promise<User | null> {
    try {
        return await getWithCredentialsJson<User>(
            `/user/user`,
            repositoryContext
        );
    } catch {
        return null;
    }
}
// Update
export async function updateProfilePicture(imageFile: File): Promise<void> {
    await uploadImage(
        imageFile,
        vars.API_ENDPOINT + "/user/profile-picture-upload"
    );
}
// Delete
