export function unwrap<T>(value: T | undefined | null, errorMessage: string) {
    if (!value) {
        throw new Error(errorMessage);
    }
    return value;
}
