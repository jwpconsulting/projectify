<script lang="ts">
    import { _ } from "svelte-i18n";
    import Header from "$lib/figma/navigation/header/Header.svelte";
    import InputField from "$lib/figma/input-fields/InputField.svelte";
</script>

<Header logoVisible={false} alwaysVisible>
    <InputField
        slot="center"
        style={{ kind: "search" }}
        placeholder={$_("dashboard.search-task")}
        name="search"
    />
</Header>
