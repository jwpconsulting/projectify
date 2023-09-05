<script lang="ts">
    import { _ } from "svelte-i18n";

    import Layout from "$lib/figma/navigation/header/Layout.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
</script>

<Layout alwaysVisible>
    <InputField
        slot="desktop-center"
        style={{ kind: "search" }}
        placeholder={$_("dashboard.search-task")}
        name="search"
    />
</Layout>
