import type { SvelteComponent } from "svelte";
import type { BaseAnnotations } from "@storybook/addons";

type DecoratorReturnType =
    | void
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
