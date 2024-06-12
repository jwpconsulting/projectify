// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
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
