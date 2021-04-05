<script lang="ts">
    export let small: boolean = false;
</script>

<div
    class="flex-col-container 
        md:pl-4 md:pr-8 md:pt-4 md:pb-8 
        mx-auto w-full 
        {small ? 'max-w-4xl' : 'max-w-full'}"
>
    <div
        class="flex-col-container 
            bg-white
            md:rounded-xl md:shadow 
            overflow-hidden"
    >
        <nav
            class="flex flex-col gap-y-2 md:flex-row 
                items-center justify-between 
                border-b border-dashed border-gray-400
                p-4"
        >
            <slot name="breadcrumbs" />
            <slot name="buttons" />
        </nav>

        <slot />

        <footer
            class="w-full bg-gray-800 text-gray-300 text-center text-sm p-5"
        >
            <span> © Ebisu Flashcards 2021. Made with ❤ and </span>
            <a class="hover:underline" href="https://svelte.dev/"> Svelte </a>
            /
            <a class="hover:underline" href="https://svelte.dev/">
                SvelteKit
            </a>
            <span>.</span>
        </footer>
    </div>
</div>
