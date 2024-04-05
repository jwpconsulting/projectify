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
import type { BaseAnnotations } from "@storybook/addons";
import type { SvelteComponent } from "svelte";

import type { ArgType } from "$lib/storybook";

type DecoratorReturnType =
    | SvelteComponent
    | {
          Component: unknown;
          props?: unknown;
      };

declare module "@storybook/addon-svelte-csf" {
    interface StoryProps
        extends BaseAnnotations<unknown, DecoratorReturnType> {
        id?: string;
        name: string;
        template?: string;
        source?: boolean | string;

        args?: unknown;
    }
}

// XXX oh no, a very hacky override
declare module "@storybook/svelte" {
    interface Meta {
        component: Component;
        argTypes?: Record<str, ArgType>;
        args?: Record<str, unknown>;
        parameters?: Record<str, unknown>;
    }
    interface StoryObj {
        args?: Record<str, unknown>;
        parameters?: Record<str, unknown>;
    }
}
