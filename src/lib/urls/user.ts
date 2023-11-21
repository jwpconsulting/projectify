export const logInUrl = "/user/log-in";
export const logOutUrl = "/user/log-out";
export const signUpUrl = "/user/sign-up";
export const requestPasswordResetUrl = "/user/request-password-reset";
export const sentEmailConfirmationLinkUrl =
    "/user/sent-email-confirmation-link";

export function getLogInWithNextUrl(next: string): string {
    const encoded = encodeURIComponent(next);
    return `/user/log-in?next=${encoded}`;
}
