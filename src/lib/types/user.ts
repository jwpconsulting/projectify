export interface User {
    email: string;
    // TODO should be undefined
    profile_picture: string | null;
    full_name?: string;
}

export function getDisplayName(user: User): string {
    if (user.full_name) {
        return user.full_name;
    }
    return user.email;
}
