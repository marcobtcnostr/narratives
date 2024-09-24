// src\lib\stores\stores.ts
import { writable } from 'svelte/store';
import Home from '$lib/components/pages/Home.svelte';

export const currentComponent = writable(Home);

function createOrientationStore() {
    const { subscribe, set } = writable('portrait'); // Default value

    function determineOrientation() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        if (width > height) {
            set('landscape');
        } else {
            set('portrait');
        }
    }

    window.addEventListener('resize', determineOrientation);
    determineOrientation(); // Initialize at load

    return {
        subscribe
    };
}

export const orientation = createOrientationStore();
