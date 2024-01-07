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
// This will prevent svelte-kit from complaining about us calling
// fetch from within a load() fn. Even though we do retrieve the current
// workspace using the svelte kit provided fetch, in the page itself
// we subscribe to archived workspace boards, which in turn will fire off
// another fetch request -- this time using window.fetch. Since svelte kit
// will attempt to render this page in the server too, we have to be extra
// sure that it won't attempt it. Hence this line here:
export const ssr = false;
