<script lang="ts">
    import { _ } from "svelte-i18n";

    import PageLayout from "$lib/components/layouts/pageLayout.svelte";
</script>

<PageLayout>
    <main
        class="flex grow flex-col items-center justify-center bg-base-200 p-4"
    >
        <h1 class="pb-2 text-6xl">{$_("404")}</h1>
        <div class="font-bold">{$_("page-not-found")}</div>
        <div class="text-sm">
            {$_("the-page-you-are-looking-for-could-not-be-found")}
        </div>
        <a href="/" class="btn-action btn btn-md m-3 rounded-full px-8"
            >{$_("go-back")}</a
        >
    </main>
</PageLayout>
