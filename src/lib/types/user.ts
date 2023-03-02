export type User = {
    email: string;
    profile_picture?: string;
    full_name?: string;
};

export function getDisplayName(user: User): string {
    if (user.full_name) {
        return user.full_name;
    }
    return user.email;
}
