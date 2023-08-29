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
