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
export interface TimestampedType {
    created: string;
    modified: string;
}

export interface TitleDescriptionType {
    title: string;
    description?: string;
}

export type SearchInput = string | undefined;

// https://stackoverflow.com/questions/65332597/typescript-is-there-a-recursive-keyof/65334052#65334052
export type RecursiveKeyOf<TObj extends object> =
    // Create an object type from `TObj`, where all the individual
    // properties are mapped to a string type if the value is not an object
    // or union of string types containing the current and descendant
    // possibilities when it's an object type.
    {
        // Does this for every property in `TObj` that is a string or number
        [TKey in keyof TObj & (string | number)]: RecursiveKeyOfHandleValue<
            TObj[TKey],
            `${TKey}`
        >;
        // for every string or number property name // Now flatten the object's property types to a final union type
    }[keyof TObj & (string | number)];

// This type does the same as `RecursiveKeyOf`, but since
// we're handling nested properties at this point, it creates
// the strings for property access and index access
type RecursiveKeyOfInner<TObj extends object> = {
    [TKey in keyof TObj & (string | number)]: RecursiveKeyOfHandleValue<
        TObj[TKey],
        `['${TKey}']` | `.${TKey}`
    >;
}[keyof TObj & (string | number)];

type RecursiveKeyOfHandleValue<TValue, Text extends string> =
    // If the value is an array then ignore it, providing back
    // only the passed in text
    TValue extends object[]
        ? Text
        : // If the value is an object...
        TValue extends object
        ? // Then...
          // 1. Return the current property name as a string
          | Text
              // 2. Return any nested property text concatenated to this text
              | `${Text}${RecursiveKeyOfInner<TValue>}`
        : // Else, only return the current text as a string
          Text;

// Lol monads
export type Result<Ok, Error> =
    | { ok: true; result: Ok }
    | { ok: false; error: Error };
