<script lang="ts">
    import InputField from "$lib/figma/input-fields/InputField.svelte";
    import { inputFieldSizes } from "$lib/figma/types";
    import type { InputFieldStyle } from "$lib/figma/types";
    import { fc, fr } from "$lib/storybook";

    const inputFieldStyles: InputFieldStyle[] = [
        { kind: "search" },
        { kind: "subTask" },
        { kind: "field", inputType: "text" },
        { kind: "field", inputType: "password" },
    ];
</script>

<div class={fc}>
    {#each inputFieldSizes as size}
        <div class={fr}>
            <div class="capitalize">
                {size}
            </div>
            <div class={fc}>
                {#each inputFieldStyles as style}
                    <div class={`${fr} items-center`}>
                        <div class="capitalize">
                            {style.kind}
                            {style.kind === "field"
                                ? `(${style.inputType})`
                                : ""}
                        </div>
                        <div class="w-96">
                            <InputField
                                {style}
                                label="email"
                                anchorTop={{
                                    href: "/",
                                    label: "Change email",
                                }}
                                anchorBottom={{
                                    href: "/",
                                    label: "Forgot password?",
                                }}
                                name={`email ${size} ${JSON.stringify(style)}`}
                                placeholder="Enter input"
                            />
                        </div>
                    </div>
                {/each}
            </div>
        </div>
    {/each}
</div>
