import type { User } from "$lib/types/user";
import { getWithCredentialsJson } from "$lib/repository/util";
import type { RepositoryContext } from "$lib/types/repository";

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
