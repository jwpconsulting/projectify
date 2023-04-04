import type { SvelteComponent } from "svelte";
import type { BaseAnnotations } from "@storybook/addons";

type DecoratorReturnType =
    | void
    | SvelteComponent
    | {
          Component: any;
          props?: any;
      };

declare module "@storybook/addon-svelte-csf" {
    interface StoryProps extends BaseAnnotations<any, DecoratorReturnType> {
        id?: string;
        name: string;
        template?: string;
        source?: boolean | string;

        args?: any;
    }
}
