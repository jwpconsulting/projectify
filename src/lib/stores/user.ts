import { writable } from "svelte/store";
import { client } from "$lib/graphql/client";

import {
    Mutation_Singup,
    Mutation_EmailConfirmation,
    Mutation_Login,
    Mutation_Logout,
    Query_User,
} from "$lib/graphql/operations";
import { goto } from "$app/navigation";

export const user = writable(null);
export const userIsLoading = writable(false);
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

            console.log("singinRedirect.to", singinRedirect.to);

            if (singinRedirect.to) {
                console.log("redirect to ", singinRedirect.to);

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
    userIsLoading.set(false);
};

export const fetchUser = async () => {
    userIsLoading.set(true);
    try {
        const res = await client.query({
            query: Query_User,
        });

        if (res.data.user !== null) {
            const userData = res.data.user;
            user.set(userData);
            return userData;
        }
    } catch (error) {
        console.log(error);
    }
    userIsLoading.set(false);
    return null;
};
