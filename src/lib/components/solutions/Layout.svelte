<!-- Common layout for solution layouts -->
<div class="flex flex-col items-center gap-20 pb-20">
    <slot name="hero" />
    <div class="flex max-w-3xl flex-col gap-6 px-8 sm:mx-16 sm:gap-16">
        <slot name="content" />
    </div>
</div>
