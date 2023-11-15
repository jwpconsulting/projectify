<!-- Common layout for solution layouts -->
<div class="flex flex-col items-center gap-20 pb-20">
    <div class="flex w-full flex-col items-center bg-background p-6 sm:p-16">
        <div class="w-full max-w-3xl">
            <slot name="hero" />
        </div>
    </div>
    <div class="w-full max-w-3xl p-6">
        <slot name="content" />
    </div>
</div>
