import { writable } from "svelte/store";
import { goto } from "$app/navigation";
import { client } from "$lib/graphql-client";
import { gql } from "graphql-request";

export const user = writable(null);
export const singinRedirect = { to: null };

user.subscribe((u) => {
    if (u) {
        if (singinRedirect.to == null) {
            goto("/");
        } else {
            goto(singinRedirect.to);
            singinRedirect.to = null;
        }
    }
});

export const logout = async () => {
    try {
        await client.request(
            gql`
                mutation {
                    logout {
                        user {
                            email
                        }
                    }
                }
            `
        );
    } catch (error) {
        console.error(error);
    }

    user.set(null);
};
