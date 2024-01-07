// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2024 JWP Consulting GK
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
/*
 * Block scrolling until the callback that is returned is called
 * This might not be compatible with other functions that change
 * document body style or scroll.
 */
export function blockScrolling(): () => void {
    const scrollOffset = window.scrollY;
    document.body.style.position = "fixed";
    document.body.scroll(0, scrollOffset);
    return () => {
        document.body.style.position = "";
        window.scrollTo(0, scrollOffset);
    };
}
