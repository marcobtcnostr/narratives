// src\lib\utils\utils.ts

import { writable } from 'svelte/store';

export function createPersistentStore(key, startValue) {
    const isClient = typeof window !== 'undefined';

    let data = startValue;

    if (isClient) {
        const storedValue = localStorage.getItem(key);

        // console.log(`[createPersistentStore] Check local storage for ${key}:`, storedValue !== null);

        if (storedValue !== null) {
            // Parse the stored string as an array and convert to Set if the startValue is an instance of Set
            if (startValue instanceof Set) {
                data = new Set(JSON.parse(storedValue));
                // console.log(`[createPersistentStore] Loaded and converted to Set from localStorage for ${key}:`, data);
            } else {
                data = JSON.parse(storedValue);
                // console.log(`[createPersistentStore] Loaded JSON from localStorage for ${key}:`, data);
            }
        } else {
            // console.log(`[createPersistentStore] No stored value for ${key}, using initial:`, startValue);
            // If no value in storage, set the initial value based on its type
            if (startValue instanceof Set) {
                // console.log(`[createPersistentStore] Storing initial Set in localStorage for ${key}:`, [...startValue]);
                localStorage.setItem(key, JSON.stringify([...startValue]));  // Serialize Set as an array
            } else {
                // console.log(`[createPersistentStore] Storing initial JSON in localStorage for ${key}:`, startValue);
                localStorage.setItem(key, JSON.stringify(startValue));  // Serialize other types directly
            }
        }
    }

    const store = writable(data, () => {
        if (isClient) {
            return store.subscribe((value) => {
                // console.log(`[createPersistentStore] Current store value for ${key}:`, value);

                if (value instanceof Set) {
                    // console.log(`[createPersistentStore] Stored Set as array in localStorage for ${key}:`, [...value]);
                    localStorage.setItem(key, JSON.stringify([...value]));
                } else {
                    // console.log(`[createPersistentStore] Stored JSON in localStorage for ${key}:`, value);
                    localStorage.setItem(key, JSON.stringify(value));
                }
            });
        }
    });

    return store;
}

export function createSessionStore(key, initialValue) {
    const savedValue = sessionStorage.getItem(key);
    const initial = savedValue ? JSON.parse(savedValue) : initialValue;
    const { subscribe, set } = writable(initial);

    return {
        subscribe,
        set: (newValue) => {
            console.log(`Setting ${key}:`, newValue);
            sessionStorage.setItem(key, JSON.stringify(newValue));
            set(newValue);
        },
        reset: () => {
            sessionStorage.removeItem(key);
            set(initialValue);
        }
    };
}

export function truncatedBech32(bech32, length) {
    return `${bech32.substring(0, length || 9)}...`;
}
