// src\lib\stores\narratives-stores.ts

import { writable, derived } from 'svelte/store';
import type { NarrativesDB, PublisherOption } from '$lib/types/narratives-types'
import { groupNarrativesByDatePublishedAndPublisher } from '$lib/utils/narratives-utils';
import { createPersistentStore, createSessionStore } from '$lib/utils/utils';

export const narrativesStore = writable<NarrativesDB[]>([]);
export const narrativesPostStore = writable<NarrativesDB[]>([]);

export const narrativesPublisherOptionsStore = writable<PublisherOption[]>([]);

export const groupedNarrativesByDatePublishedAndPublisherStore = derived(
  narrativesStore,
  ($narrativesStore) => {
    return groupNarrativesByDatePublishedAndPublisher($narrativesStore);
  }
);

const initialFilters = {
  publishers: ['BBC News', 'CNBC'],
  platforms: ['Web', 'Nostr', 'Twitter'],
  countries: ['United Kingdom', 'United States of America'],
  // macro_topics: ['House prices'],
  dateAddedRange: { start: '1900-01-01 00:00:00', end: '2050-01-01 23:59:59' },
  datePublishedRange: { start: '2024-01-01 00:00:00', end: '2025-01-01 23:59:59' }
};

export const selectedNarrativesFiltersStore = createPersistentStore('selectedNarrativesFilters', initialFilters);

export const selectedContentIDStore = writable('');

export const isNarrativesFilterWindowOpen = writable(false);
export const isNarrativesDatabaseWindowOpen = writable(false);
export const isNarrativesDatabaseAddWindowOpen = writable(false);
export const isShareNarrativesPostWindowOpen = writable(false);
export const isUpdatingDatabase = writable(false);

export const serverUrl = createSessionStore('serverUrl', 'http://localhost:5000');