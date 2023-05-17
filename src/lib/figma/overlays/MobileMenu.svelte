<script lang="ts">
    import { _ } from "svelte-i18n";
    import Button from "$lib/funabashi/buttons/Button.svelte";
</script>

<div class="mb-8 flex flex-col divide-y divide-border p-4">
    <div class="py-2">
        <a href="/features">
            <Button
                style={{ kind: "tertiary", icon: null }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.features")}
            />
        </a>
    </div>
    <div class="py-2">
        <Button
            style={{ kind: "tertiary", icon: null }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("header.solutions")}
        />
    </div>
    <div class="py-2">
        <Button
            style={{ kind: "tertiary", icon: null }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("header.resources")}
        />
    </div>
    <div class="py-2">
        <Button
            style={{ kind: "tertiary", icon: null }}
            color="blue"
            disabled={false}
            size="medium"
            label={$_("header.company")}
        />
    </div>
    <div class="py-2">
        <a href="/pricing">
            <Button
                style={{ kind: "tertiary", icon: null }}
                color="blue"
                disabled={false}
                size="medium"
                label={$_("header.pricing")}
            />
        </a>
    </div>
</div>
