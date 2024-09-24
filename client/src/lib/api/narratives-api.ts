// src\lib\api\narratives_api.ts

import { get } from 'svelte/store';
import { narrativesStore, narrativesPublisherOptionsStore, selectedNarrativesFiltersStore, serverUrl } from '$lib/stores/narratives-stores';
import type { NarrativesFilterOptions, PublisherOption } from '$lib/types/narratives-types';


// const SERVER_URL = get(serverUrl);

async function fetchData(url: string, options = {}): Promise<any> {
    const fullUrl = `${get(serverUrl)}${url}`; // Prepend the server URL to the endpoint path
    try {
        const response = await fetch(fullUrl, options);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

export async function fetchNarrativesData(filters: NarrativesFilterOptions = {}): Promise<void> {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ filters }), // Send the filters as part of the request body
    };
    try {
        const data = await fetchData('/fetch-narratives-data', options);
        narrativesStore.set(data); // Update the store with the fetched data
    } catch (error) {
        console.error('Error fetching narratives:', error);
        narrativesStore.set([]); // Clear the store or set an error state as needed
    }
}

export async function updateNarrativesDatabase(): Promise<void> {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // If you need to send data, include a body:
        // body: JSON.stringify({ someData: "example data" }),
    };
    try {
        const updatedData = await fetchData('/update-narratives-database', options);
        console.log('Database updated:', updatedData);
        // Update the publisher options first
        await fetchNarrativesPublisherOptions();

        // Fetch the current filters from the store
        const currentFilters = get(selectedNarrativesFiltersStore);

        // Fetch narratives data with the current filters
        await fetchNarrativesData(currentFilters);
    } catch (error) {
        console.error('Error updating the database:', error);
        // Optionally set the store to an error state or keep the old data
        // narrativesDbStore.set([]); // Clear the store or set an error state as needed
    }
}

export async function fetchNarrativesPublisherOptions(): Promise<void> {
    try {
        const publisherOptions = await fetchData('/fetch-publisher-options', { method: 'GET' });
        narrativesPublisherOptionsStore.set(publisherOptions); // Update the store with the fetched data
    } catch (error) {
        console.error('Error fetching publisher options:', error);
        narrativesPublisherOptionsStore.set([]); // Clear the store or set an error state as needed
    }
}

// Function to update publisher options in the backend
export async function editPublisherOptions(publisherOptions: PublisherOption[]): Promise<void> {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ publisherOptions }), // Sending the entire list of updated options
    };
    try {
        await fetchData('/edit-publisher-options', options);
        // Handle success if needed (e.g., refresh data)
        await fetchNarrativesData();
    } catch (error) {
        console.error('Error updating publisher options:', error);
        throw error; // Re-throw or handle as needed
    }
}

// Function to add a new content ID to the server
export async function addContentId(contentId: string): Promise<void> {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content_id: contentId }),
    };
    try {
        const response = await fetchData('/add-content-id', options);
        const result = await response.json();
        console.log(result.message); // Log the success message
    } catch (error) {
        console.error('Failed to add content ID:', error);
        throw error; // Re-throw to handle it in the Svelte component
    }
}

export async function updateContentIdTopic(contentId: string, newTopic: string): Promise<void> {
    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content_id: contentId, topic: newTopic }), // Send the content ID and new topic
    };
  
    try {
      await fetchData('/update-content-id-topic', options);
      console.log('Article topic updated successfully');
    } catch (error) {
      console.error('Failed to update article topic:', error);
      throw error;
    }
  }
  

export async function chatWithOpenAIAssistant(message: string): Promise<string> {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
    };
    const response = await fetchData('/chat-with-openai-assistant', options);
    return response.response; // Assuming the server response has a 'response' field with the chatbot's message
}

export async function closeOpenAIChat(): Promise<void> {
    await fetchData('/close-openai-chat', { method: 'POST' });
}

export async function loadContentForOpenAIChatbot(contentIds: string[]): Promise<void> {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content_ids: contentIds }),
    };
    await fetchData('/load-content-for-openai-chatbot', options);
}

export async function fetchApiKeys(): Promise<any> {
    try {
        const apiKeys = await fetchData('/fetch-api-keys', { method: 'GET' });
        return apiKeys;
    } catch (error) {
        console.error('Error fetching API keys:', error);
        throw error;
    }
}

export async function updateApiKey(api: string, key: string): Promise<void> {
    const options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ api, key }),
    };
    try {
        await fetchData('/update-api-key', options);
        console.log('API key updated successfully');
    } catch (error) {
        console.error('Error updating API key:', error);
        throw error;
    }
}