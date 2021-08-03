import sveltePreprocess from "svelte-preprocess";
import nodeAdapter from "@sveltejs/adapter-node";

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://github.com/sveltejs/svelte-preprocess
    // for more information about preprocessors
    preprocess: [
        sveltePreprocess({
            defaults: {
                style: "postcss",
            },
            postcss: true,
        }),
    ],
    kit: {
        // By default, `npm run build` will create a standard Node app.
        // You can create optimized builds for different platforms by
        // specifying a different adapter
        adapter: nodeAdapter(),

        // hydrate the <div id="svelte"> element in src/app.html
        target: "#svelte",
    },
};

export default config;