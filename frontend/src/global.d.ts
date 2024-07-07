// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2021-2024 JWP Consulting GK
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
/// <reference types="@sveltejs/kit" />
declare const __GIT_COMMIT_DATE__: string;
declare const __GIT_BRANCH_NAME__: string;
declare const __GIT_COMMIT_HASH__: string;
declare const __BUILD_DATE__: string;

declare const __MODE__: string;

declare const __API_ENDPOINT__: string;
declare const __WS_ENDPOINT__: string;

// Automatically generated third-party-licenses module as part of vite
// build process
declare module "third-party-licenses" {
    export = string;
}

// Used for @sveltejs/enhanced-img, images have to be loaded by appending
// ?enhanced
declare module "*.png?enhanced" {
    const value: string;
    export = value;
}

// https://www.npmjs.com/package/@poppanator/sveltekit-svg#typescript
// Copied from the packages dist/svg.d.ts file
declare module "*.svg?url" {
    const content: string;
    export default content;
}

declare module "favicon-html" {
    const content: string;
    export default content;
}
