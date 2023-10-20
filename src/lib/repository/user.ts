import vars from "$lib/env";
import { getWithCredentialsJson } from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";
import type { User } from "$lib/types/user";
import { uploadImage } from "$lib/utils/file";

// Create
// Read
export async function getUser(
    repositoryContext: RepositoryContext
): Promise<User | undefined> {
    const response = await getWithCredentialsJson<User>(
        `/user/user`,
        repositoryContext
    );
    if (response.ok) {
        return response.data;
    } else if (response.kind === "forbidden") {
        return undefined;
    }
    console.error(response);
    throw new Error("There was a problem retrieving the user");
}
// Update
export async function updateProfilePicture(imageFile: File): Promise<void> {
    await uploadImage(
        imageFile,
        vars.API_ENDPOINT + "/user/profile-picture-upload"
    );
}
// Delete
