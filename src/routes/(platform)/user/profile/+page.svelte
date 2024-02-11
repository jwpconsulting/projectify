<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { updateUserProfile } from "$lib/stores/user";

    import type { PageData } from "./$types";

    export let data: PageData;

    let { user } = data;
    let preferredName = user.preferred_name ?? undefined;

    $: hasProfilePicture =
        imageFile !== undefined || user.profile_picture !== null;

    let state: "viewing" | "editing" | "saving" = "viewing";
    let imageFile: File | undefined = undefined;

    function fileSelected(file: File, src: string) {
        state = "editing";
        imageFile = file;
        user.profile_picture = src;
    }

    async function save() {
        state = "saving";
        const picture =
            imageFile !== undefined
                ? { kind: "update" as const, imageFile }
                : user.profile_picture === null
                ? { kind: "clear" as const }
                : { kind: "keep" as const };
        // TODO handle validation errors
        user = await updateUserProfile(preferredName, picture, { fetch });
        // TODO show confirmation flash when saving complete Justus
        // 2023-08-03
        state = "viewing";
        imageFile = undefined;
    }

    function removePicture() {
        state = "editing";
        user.profile_picture = null;
        imageFile = undefined;
    }

    function cancel() {
        state = "viewing";
        preferredName = user.preferred_name ?? undefined;
        user = data.user;
    }
</script>

<figure class="flex flex-col items-center gap-7">
    <div class="relative flex w-max flex-col">
        <AvatarVariant size="large" content={{ kind: "single", user }} />
        <div class="absolute -bottom-1/4 -right-1/4">
            <UploadAvatar
                {fileSelected}
                label={$_(
                    "user-account-settings.overview.profile-picture.prompt",
                )}
            />
        </div>
    </div>
    <figcaption>
        {$_("user-account-settings.overview.profile-picture.current")}
    </figcaption>
</figure>
<Button
    action={{
        kind: "button",
        action: removePicture,
        disabled: !hasProfilePicture || state === "saving",
    }}
    size="medium"
    color="blue"
    style={{ kind: "primary" }}
    label={$_("user-account-settings.overview.profile-picture.remove")}
/>
<div class="flex flex-col gap-10">
    <div class="flex flex-col gap-4">
        <InputField
            label={$_("user-account-settings.overview.preferred-name.label")}
            placeholder={$_(
                "user-account-settings.overview.preferred-name.placeholder",
            )}
            name="preferred-name"
            bind:value={preferredName}
            style={{ inputType: "text" }}
            readonly={state !== "editing"}
            onClick={() => {
                state = "editing";
            }}
        />
    </div>
    <div class="flex flex-col gap-2">
        <Button
            action={{
                kind: "button",
                action: save,
                disabled: state !== "editing",
            }}
            size="medium"
            color="blue"
            style={{ kind: "primary" }}
            label={$_("user-account-settings.overview.save")}
        />
        <Button
            action={{
                kind: "button",
                action: cancel,
                disabled: state !== "editing",
            }}
            size="medium"
            color="blue"
            style={{ kind: "secondary" }}
            label={$_("user-account-settings.overview.cancel")}
        />
        <Button
            action={{
                kind: "button",
                action: console.error.bind(
                    null,
                    "Delete account not implemented",
                ),
            }}
            size="medium"
            color="red"
            style={{ kind: "secondary" }}
            label={$_("user-account-settings.overview.delete-account")}
        />
        <Anchor
            href="/user/profile/change-password"
            size="normal"
            label={$_("user-account-settings.overview.change-password")}
        />
        <Anchor
            href="/user/profile/update-email"
            size="normal"
            label={$_("user-account-settings.overview.update-email")}
        />
    </div>
</div>
