// src\lib\utils\social-utils.ts

import type NDK from '@nostr-dev-kit/ndk';
import { NDKUser } from '@nostr-dev-kit/ndk';
import { NDKNip07Signer, NDKPrivateKeySigner } from '@nostr-dev-kit/ndk';
import { nip19 } from 'nostr-tools';
import { currentUser, userFollows } from '$lib/stores/social-stores';
import { get as getStore } from 'svelte/store';


export async function login(ndk: NDK, key: string, method: 'nsec' | 'nip07'): Promise<NDKUser | null> {
    const currentUserNpub = localStorage.getItem('currentUserNpub');
    let user: NDKUser | null = currentUserNpub ? new NDKUser({ npub: currentUserNpub, ndk }) : null;

    if (method === 'nsec') {
        try {
            const result = nip19.decode(key);
            if (!result.data) {
                console.error('Decoding failed or invalid nsec key');
                return null;
            }
            const privateKey = result.data;
            ndk.signer = new NDKPrivateKeySigner(privateKey);
            return await ndk.signer.user();
        } catch (e) {
            console.error('Error during private key login:', e);
            return null;
        }
    } else if (method === 'nip07') {
        try {
            ndk.signer = new NDKNip07Signer();
            user = await ndk.signer.user();
            if (user) {
                console.log('NIP-07 login successful:', user);
                return user;
            } else {
                console.log('NIP-07 login returned no user');
                return null;
            }
        } catch (e) {
            console.error('Error during NIP-07 login:', e);
            return null;
        }
    }

    return null;
}

export async function prepareSession(user: NDKUser): Promise<void> {
    currentUser.set(user);  // Set the current user in the store
    try {
        // console.log('user:', user);

        // const userProfile = await user.fetchProfile();
        // console.log('userProfile:', userProfile);

        const follows = await user.follows();
        // console.log('follows:', follows);

        userFollows.update(currentFollows => {
            currentFollows.clear();

            follows.forEach(follow => currentFollows.add(follow));

            return new Set(currentFollows);
        });

        getStore(userFollows)
        // console.log('userFollows:', getStore(userFollows));

    } catch (e) {
        console.error('Error during session preparation:', e);
    }
}

export async function clearCache() {
    if (!('indexedDB' in window)) {
        console.error('IndexedDB is not supported on this browser.');
        return;
    }

    const dbName = 'myAppCache'; // Example DB name used by NDKCacheAdapter
    const request = indexedDB.open(dbName);

    request.onerror = function(event) {
        console.error('Error opening IndexedDB:', event.target.errorCode);
    };

    request.onsuccess = function(event) {
        const db = event.target.result;
        const transaction = db.transaction(db.objectStoreNames, 'readwrite');
        transaction.onerror = function(event) {
            console.error('Transaction error:', event.target.errorCode);
        };

        Array.from(db.objectStoreNames).forEach(storeName => {
            const objectStore = transaction.objectStore(storeName);
            const clearRequest = objectStore.clear();
            clearRequest.onsuccess = function() {
                console.log(`Cleared object store: ${storeName}`);
            };
            clearRequest.onerror = function(event) {
                console.error('Clear request error:', event.target.errorCode);
            };
        });
    };
}