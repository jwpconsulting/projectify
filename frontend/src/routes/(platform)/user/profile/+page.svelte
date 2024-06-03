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
    import type { BeforeNavigate } from "@sveltejs/kit";
    import { _ } from "svelte-i18n";

    import UploadAvatar from "$lib/figma/buttons/UploadAvatar.svelte";
    import AvatarVariant from "$lib/figma/navigation/AvatarVariant.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import InputField from "$lib/funabashi/input-fields/InputField.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import { updateUserProfile } from "$lib/stores/user";
    import { changePasswordUrl, updateEmailAddressUrl } from "$lib/urls/user";

    import type { PageData } from "./$types";

    import { beforeNavigate } from "$app/navigation";
    import { openApiClient } from "$lib/repository/util";

    export let data: PageData;

    let { user } = data;
    let preferred_name = user.preferred_name;

    let state: "viewing" | "editing" | "saving" = "viewing";
    let picture:
        | { kind: "keep" }
        | { kind: "clear" }
        | { kind: "update"; file: File; src: string } = { kind: "keep" };

    function fileSelected(file: File, src: string) {
        startEditing();
        picture = { kind: "update", file, src };
    }

    async function save() {
        state = "saving";
        if (picture.kind !== "keep") {
            const formData = new FormData();
            if (picture.kind === "update") {
                formData.append("file", picture.file);
            }
            const { response, error } = await openApiClient.POST(
                "/user/user/profile-picture/upload",
                { body: {}, bodySerializer: () => formData },
            );
            if (!response.ok) {
                console.error(error);
                throw new Error("Error when upload picture");
            }
        }
        // TODO handle validation errors
        user = await updateUserProfile(preferred_name);
        finishEditing();
    }

    function removePicture() {
        startEditing();
        picture = { kind: "clear" };
    }

    function startEditing() {
        state = "editing";
    }

    function finishEditing() {
        // TODO show confirmation flash when saving complete Justus
        // 2023-08-03
        resetForm();
    }

    function cancelEditing() {
        resetForm();
    }

    function resetForm() {
        state = "viewing";
        picture = { kind: "keep" };
        preferred_name = user.preferred_name;
    }

    beforeNavigate((navigation: BeforeNavigate) => {
        if (state == "editing") {
            const navigateAway = window.confirm(
                $_("user-account-settings.overview.confirm-navigate-away"),
            );
            if (!navigateAway) {
                navigation.cancel();
            }
        }
    });

    $: renderProfilePicture = {
        ...user,
        preferred_name,
        profile_picture:
            picture.kind === "keep"
                ? user.profile_picture
                : picture.kind === "clear"
                ? null
                : picture.src,
    };

    $: console.log(renderProfilePicture);

    $: canRemoveProfilePicture =
        user.profile_picture !== null &&
        ["keep", "update"].includes(picture.kind);
</script>

<form class="flex flex-col gap-10" on:submit|preventDefault={save}>
    <figure class="flex flex-col items-center gap-7">
        <div class="relative flex w-max flex-col">
            <AvatarVariant
                size="large"
                content={{ kind: "single", user: renderProfilePicture }}
            />
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
            disabled: !canRemoveProfilePicture,
        }}
        size="medium"
        color="blue"
        style={{ kind: "primary" }}
        label={$_("user-account-settings.overview.profile-picture.remove")}
    />
    <div class="flex flex-col gap-4">
        <div class="flex flex-col gap-1">
            <p class="font-bold">
                {$_(
                    "user-account-settings.overview.current-email-address.label",
                )}
            </p>
            <p>
                {user.email}
            </p>
            <p>
                <Anchor
                    href={updateEmailAddressUrl}
                    size="normal"
                    label={$_(
                        "user-account-settings.overview.current-email-address.update-email-address",
                    )}
                />
            </p>
        </div>
        <InputField
            label={$_("user-account-settings.overview.preferred-name.label")}
            placeholder={$_(
                "user-account-settings.overview.preferred-name.placeholder",
            )}
            name="preferred-name"
            bind:value={preferred_name}
            style={{ inputType: "text" }}
            readonly={state !== "editing"}
            onClick={startEditing}
        />
    </div>
    <div class="flex flex-col gap-2">
        <Button
            action={{
                kind: "submit",
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
                action: cancelEditing,
                disabled: state !== "editing",
            }}
            size="medium"
            color="blue"
            style={{ kind: "secondary" }}
            label={$_("user-account-settings.overview.cancel")}
        />
    </div>
</form>
<div class="flex flex-col gap-2">
    <h3 class="font-bold">
        {$_("user-account-settings.overview.other-actions.title")}
    </h3>
    <Anchor
        href={changePasswordUrl}
        size="normal"
        label={$_(
            "user-account-settings.overview.other-actions.change-password",
        )}
    />
</div>
<div class="flex flex-col gap-2">
    <h3 class="font-bold">
        {$_("user-account-settings.overview.delete-account.title")}
    </h3>
    <p>
        {$_("user-account-settings.overview.delete-account.message")}
    </p>
    <p>
        <Anchor
            label={$_("user-account-settings.overview.delete-account.label")}
            href={$_("user-account-settings.overview.delete-account.email")}
            size="normal"
        />
    </p>
</div>
