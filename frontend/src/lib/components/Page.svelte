<script lang="ts">
    export let small: boolean = false;
</script>

<div class="flex-grow flex flex-col container bg-white md:mx-auto md:rounded-xl md:shadow overflow-hidden " class:max-w-xl={small} >
    <nav class="flex items-center justify-between bg-white border-b border-dashed border-gray-400 p-4">
        <slot name="breadcrumbs"/>
        <slot name="buttons"/>
    </nav>
    
    <slot />
    
    
    <footer class="w-full bg-gray-800 text-gray-300 text-center text-sm p-5">
        <span>
            © Ebisu Flashcards 2020. Made with ❤ and 
        </span>
        <a class="hover:underline" href="https://svelte.dev/">
            Svelte
        </a>
        /
        <a class="hover:underline" href="https://svelte.dev/">
            SvelteKit
        </a>
        <span>.</span>
    </footer>
</div>