<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/funabashi/buttons/Button.svelte";
</script>

<div class="mb-8 flex flex-col divide-y divide-border p-4">
    <div class="py-2">
        <Button
            action={{ kind: "a", href: "/features" }}
            style={{ kind: "tertiary", icon: null }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("header.features")}
        />
    </div>
    <div class="py-2">
        <Button
            action={{ kind: "a", href: "/solutions" }}
            style={{ kind: "tertiary", icon: null }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("header.solutions")}
        />
    </div>
    <div class="py-2">
        <Button
            action={{ kind: "a", href: "/help" }}
            style={{ kind: "tertiary", icon: null }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("header.resources")}
        />
    </div>
    <div class="py-2">
        <Button
            action={{ kind: "a", href: "/pricing" }}
            style={{ kind: "tertiary", icon: null }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("header.pricing")}
        />
    </div>
</div>
