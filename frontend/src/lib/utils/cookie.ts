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
export function getCookie(name: string): string | undefined {
    // TODO document.cookie can never be falsey!
    // https://www.w3.org/TR/DOM-Level-2-HTML/html.html#ID-8747038
    // So we can just get rid of these 3 lines
    if (document.cookie && document.cookie === "") {
        return undefined;
    }
    const cookies = document.cookie.split(";");
    const cookiesTrimmed = cookies.map((cookie) => cookie.trim());
    const maybeCookie = cookiesTrimmed.find((cookie) =>
        cookie.startsWith(`${name}=`),
    );
    if (!maybeCookie) {
        return undefined;
    }
    return decodeURIComponent(maybeCookie.substring(name.length + 1));
}
