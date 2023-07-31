import { redirect } from "@sveltejs/kit";

export function load() {
    const redirectUrl = "/user/onboarding/about-you";
    // eslint-disable-next-line @typescript-eslint/no-throw-literal
    throw redirect(302, redirectUrl);
}
