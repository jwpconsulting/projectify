import { writable } from "svelte/store";
import { goto } from "$app/navigation";
import { client } from "$lib/graphql-client";

import {
    Mutation_Singup,
    Mutation_EmailConfirmation,
    Mutation_Login,
    Mutation_Logout,
} from "$lib/grapql/mutations";

export const user = writable(null);
export const singinRedirect = { to: null };

export const singUp = async (email, password) => {
    try {
        const res = await client.mutate({
            mutation: Mutation_Singup,
            variables: { email, password },
        });

        if (res.data.signup !== null) {
            const userData = res.data.signup.user;
            return userData;
        }
    } catch (error) {
        console.error(error);
    }
    return null;
};

export const emailConfirmation = async (email, token) => {
    try {
        const res = await client.mutate({
            mutation: Mutation_EmailConfirmation,
            variables: { email, token },
        });
        if (res.data.emailConfirmation !== null) {
            const userData = res.data.emailConfirmation.user;
            return userData;
        }
    } catch (error) {
        console.error(error);
    }
    return null;
};

export const login = async (email, password) => {
    try {
        const res = await client.mutate({
            mutation: Mutation_Login,
            variables: { email, password },
        });

        if (res.data.login !== null) {
            const userData = res.data.login.user;
            user.set(userData);
            if (singinRedirect.to == null) {
                goto("/");
            } else {
                goto(singinRedirect.to);
                singinRedirect.to = null;
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
};
