// src\lib\stores\social-stores.ts

import { writable, get } from 'svelte/store';
import NDK from '@nostr-dev-kit/ndk';
import NDKSvelte from '@nostr-dev-kit/ndk-svelte';
import { createPersistentStore, createSessionStore } from '$lib/utils/utils';
import NDKCacheAdapterDexie from '@nostr-dev-kit/ndk-cache-dexie';

let relays;
try {
    relays = localStorage.getItem('relays');
} catch (e) { /* handle storage errors */ }

let relayList: string[] = [];
if (relays) {
    relayList = JSON.parse(relays);
}

const defaultRelays = [
    'wss://relay.damus.io',
    'wss://nostr.wine/',
    'wss://relay.snort.social',
    'wss://relay.nostr.band/',
    'wss://purplepag.es/'
];

if (!relayList || !Array.isArray(relayList) || relayList.length === 0) {
    relayList = defaultRelays;
}

// const _ndk: NDK = new NDK({
//     explicitRelayUrls: relayList
// }) as NDK;

const _ndk: NDKSvelte = new NDKSvelte({
    explicitRelayUrls: relayList
}) as NDKSvelte;

_ndk.cacheAdapter = new NDKCacheAdapterDexie({ dbName: 'myAppCache' });

export const ndk = writable(_ndk);
// const ndk = writable(_ndk);
// export default ndk;

export const currentUser = createPersistentStore('currentUser', null);
export const userFollows = createPersistentStore('userFollows', new Set());

export const nsecKey = createSessionStore('nsecKey', '');