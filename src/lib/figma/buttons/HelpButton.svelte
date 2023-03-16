<script lang="ts">
    import { _ } from "svelte-i18n";
    import { Icon } from "@steeze-ui/svelte-icon";
    import { LightBulb } from "@steeze-ui/heroicons";
</script>

<a href="/help" class="w-full px-4 py-2">
    <div
        class="flex flex-row items-center gap-2 text-utility hover:text-base-content"
    >
        <Icon src={LightBulb} class="w-5" theme="outline" />
        <p class="text-xs font-bold uppercase">
            {$_("side-nav-overlay.help-tips")}
        </p>
    </div>
</a>
