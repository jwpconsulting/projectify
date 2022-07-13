import { writable } from "svelte/store";
import { client } from "$lib/graphql/client";

import {
    Mutation_Signup,
    Mutation_EmailConfirmation,
    Mutation_Login,
    Mutation_Logout,
    Mutation_RequesetPasswordReset,
    Mutation_ConfirmPasswordReset,
} from "$lib/graphql/operations";
import { getUser } from "$lib/repository";
import { goto } from "$app/navigation";
import type { User } from "$lib/types";

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
    try {
        const res = await client.mutate({
            mutation: Mutation_Login,
            variables: { input: { email, password } },
        });

        console.log(res);
        if (res.data.login !== null) {
            const userData = res.data.login;
            user.set(userData);

            if (signinRedirect.to) {
                goto(signinRedirect.to);
                signinRedirect.to = null;
            }

            return userData;
        }
    } catch (error) {
        console.error(error);
    }
    return null;
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

export const fetchUser = async () => {
    userIsLoading.set(true);
    try {
        const res = await getUser();

        const userData = res;
        user.set(userData);
        return userData;
    } catch (error) {
        console.log(error);
    }
    userIsLoading.set(false);
    return null;
};

export const requestPasswordReset = async (email: string) => {
    try {
        const res = await client.mutate({
            mutation: Mutation_RequesetPasswordReset,
            variables: { input: { email } },
        });

        if (res.data.requestPasswordReset !== null) {
            return res.data.requestPasswordReset.email;
        }
    } catch (error) {
        return { error };
    }
};

export const confirmPasswordReset = async (
    email: string,
    token: string,
    newPassword: string
): Promise<{ error: { message: string } } | null> => {
    try {
        await client.mutate({
            mutation: Mutation_ConfirmPasswordReset,
            variables: { input: { email, token, newPassword } },
        });
        return null;
    } catch (error) {
        return { error };
    }
};
