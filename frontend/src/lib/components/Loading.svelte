<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    export let size: 5 | 20 = 20;
</script>

<div class="{size === 5 ? 'h-5 w-5' : 'h-20 w-20'} text-primary">
    <svg viewBox="-50 -50 100 100" fill="none">
        <circle cx="0" cy="0" />
        <circle cx="0" cy="0" />
    </svg>
</div>

<style lang="scss">
    svg {
        position: relative;
        width: 100%;
        height: 100%;
        --stroke-size: 5px;
    }
    svg > circle {
        stroke: currentColor;
        stroke-width: var(--stroke-size);
        opacity: 1;
        border-radius: 50%;
        animation: ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
    }
    svg circle:nth-child(2) {
        animation-delay: 1s;
    }
    @keyframes ripple {
        0% {
            opacity: 1;
            r: 0px;
        }
        100% {
            opacity: 0;
            r: calc(50% - var(--stroke-size));
        }
    }
</style>
