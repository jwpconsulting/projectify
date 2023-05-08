import { writable } from "svelte/store";
import { client } from "$lib/graphql/client";
import type { RepositoryContext } from "$lib/types/repository";

import {
    Mutation_ConfirmPasswordReset,
    Mutation_EmailConfirmation,
    Mutation_Login,
    Mutation_Logout,
    Mutation_RequesetPasswordReset,
    Mutation_Signup,
} from "$lib/graphql/operations";
import { getUser } from "$lib/repository/user";
import { goto } from "$app/navigation";
import type { User } from "$lib/types/user";

export const user = writable<User | null>(null);
export const userIsLoading = writable(true);
export const signinRedirect: { to: null | string } = { to: null };

export const signUp = async (
    email: string,
    password: string
): Promise<string | null> => {
    const res = await client.mutate({
        mutation: Mutation_Signup,
        variables: { input: { email, password } },
    });

    if (res.data.signup !== null) {
        const userData = res.data.signup;
        return userData.email;
    }
    return null;
};

export const emailConfirmation = async (email: string, token: string) => {
    try {
        const res = await client.mutate({
            mutation: Mutation_EmailConfirmation,
            variables: { input: { email, token } },
        });
        if (res.data.emailConfirmation !== null) {
            const userData = res.data.emailConfirmation;
            return userData;
        }
    } catch (error) {
        console.error(error);
    }
    return null;
};

export const login = async (email: string, password: string) => {
    const res = await client.mutate({
        mutation: Mutation_Login,
        variables: { input: { email, password } },
    });

    if (res.data.login !== null) {
        const userData = res.data.login;
        user.set(userData);

        if (signinRedirect.to) {
            goto(signinRedirect.to);
            signinRedirect.to = null;
        }

        return userData;
    }
};

export const logout = async () => {
    try {
        await client.mutate({
            mutation: Mutation_Logout,
        });
        client.resetStore();
    } catch (error) {
        console.error(error);
    }
    user.set(null);
    userIsLoading.set(false);
};

export const fetchUser = async (repositoryContext?: RepositoryContext) => {
    userIsLoading.set(true);
    const userData = await getUser(repositoryContext);
    if (!userData) {
        userIsLoading.set(false);
        return null;
    }
    user.set(userData);
    return userData;
};

export const requestPasswordReset = async (email: string): Promise<void> => {
    await client.mutate({
        mutation: Mutation_RequesetPasswordReset,
        variables: { input: { email } },
    });
};

export const confirmPasswordReset = async (
    email: string,
    token: string,
    newPassword: string
): Promise<void> => {
    await client.mutate({
        mutation: Mutation_ConfirmPasswordReset,
        variables: { input: { email, token, newPassword } },
    });
};
