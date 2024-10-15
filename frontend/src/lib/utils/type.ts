// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2023 JWP Consulting GK
export function unwrap<T>(value: T | undefined | null, errorMessage: string) {
    if (!value) {
        throw new Error(errorMessage);
    }
    return value;
}

// https://stackoverflow.com/a/50769802
type Mutable<T> = {
    -readonly [P in keyof T]: Mutable<T[P]>;
};

/**
 * Type safe way of returning a mutable version of an object with
 * readonly root keys
 */
export function cloneMutable<T>(t: T): Mutable<T> {
    return structuredClone(t) as Mutable<T>;
}
