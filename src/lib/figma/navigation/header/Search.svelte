<script lang="ts">
    import { _ } from "svelte-i18n";

    import HeaderUniversal from "$lib/figma/navigation/header/HeaderUniversal.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
</script>

<HeaderUniversal alwaysVisible>
    <InputField
        slot="desktop-center"
        style={{ kind: "search" }}
        placeholder={$_("dashboard.search-task")}
        name="search"
    />
</HeaderUniversal>
