<script lang="ts">
    import { faFish } from "@fortawesome/free-solid-svg-icons/faFish";
    import FaIcon from "./FaIcon.svelte";
</script>

<div class="flex flex-col items-center">
    <!--Let's take this fish out for a swimming -->
    <FaIcon icon={faFish} size="75px" />
    <span class="text-2xl">
        <slot />
    </span>
</div>