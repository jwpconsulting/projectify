import { redirect } from "@sveltejs/kit";

export function load() {
    const redirectUrl = "/user/onboarding/about-you";
    throw redirect(302, redirectUrl);
}
