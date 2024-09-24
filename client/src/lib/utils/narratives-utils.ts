// src\lib\utils\narratives-utils.ts

import type { NarrativesDB } from '$lib/types/narratives-types';

export function groupNarrativesByDatePublishedAndPublisher(narratives: NarrativesDB[]): Record<string, any> {
    // First, group by date_published
    const groupedByDatePublished = narratives.reduce((acc, narrative) => {
        const date = narrative.date_published.split(' ')[0]; // Assuming date_published includes time and we only want the date
        if (!acc[date]) {
            acc[date] = [];
        }
        acc[date].push(narrative);
        return acc;
    }, {} as Record<string, NarrativesDB[]>);

    // Then, within each date, group by publisher and assemble the desired structure
    const groupedByDatePublishedAndPublisher = Object.keys(groupedByDatePublished).reduce((acc, date) => {
        const narrativesByDatePublished = groupedByDatePublished[date];
        const groupedByPublisher = narrativesByDatePublished.reduce((publisherAcc, narrative) => {
            const publisher = narrative.publisher;
            if (!publisherAcc[publisher]) {
                publisherAcc[publisher] = [];
            }
            publisherAcc[publisher].push(narrative);
            return publisherAcc;
        }, {} as Record<string, NarrativesDB[]>);

        // Transform the structure into the specified format, including itemOrder
        let itemCount = 1; // Initialize a running count for itemOrder
        const publishersWithContentIDs = Object.keys(groupedByPublisher).map(publisher => {
            const contents = groupedByPublisher[publisher];
            const itemOrder = contents.map(() => itemCount++);
            return {
                date_published: date,
                publisher: publisher,
                duration: contents.map(d => d.duration),
                content_ids: contents.map(d => d.content_id),
                titles: contents.map(d => d.title),
                itemOrder: itemOrder
            };
        });

        acc[date] = publishersWithContentIDs;
        return acc;
    }, {} as Record<string, any>);

    return groupedByDatePublishedAndPublisher;
}
