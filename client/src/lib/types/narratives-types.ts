// src/lib/types/narratives-types.ts

export interface NarrativesDB {
    content_id: string;
    title: string,
    publisher: string,
    author: string,
    date_published: string,
    date_added: string,
    duration: number,
    platform: string,
    transcript: string,
    summary: string,
    sentiment_analysis: number,
    macro_topic: string,
    publisher_political_orientation: string,
    country: string,
    sent_by: string,
    comments: string,
    reference_image: string
}

export interface NarrativesFilterOptions {
    publishers?: string[];
    platforms?: string[];
    countries?: string[];
    macro_topics?: string[];
    dateAddedRange?: { start: string; end: string };
    datePublishedRange?: { start: string; end: string };
}

export interface PublisherOption {
    publishers?: string;
    publishers_political_orientation?: string;
    countries?: string;
}