import { writable } from 'svelte/store';
import * as d3 from 'd3';

export const selectedYear = writable(2024);
export const congressData = writable(null); // this can not stay null

const cache = {};

// Initialization moved to YearDropdown.svelte's onMount for reliability in SSR
async function fetchYear(year) {
    if (typeof window === 'undefined') {
        console.log('fetchYear: skipping SSR fetch for year', year);
        return null;
    }
    const congressNumber = Math.ceil((year - 1788) / 2);
    if (cache[congressNumber]) {
        console.log('fetchYear: using cache for congress', congressNumber);
        return cache[congressNumber];
    }
    const url = `/data/min_by_congress/${congressNumber}.json`;
    console.log('fetchYear: fetching', url);
    try {
        const data = await d3.json(url);
        console.log('fetchYear: success! length:', Array.isArray(data) ? data.length : 'not-array');
        cache[congressNumber] = data;
        return data;
    } catch (err) {
        console.error('fetchYear: fetch failed for', url, err);
        return null;
    }
}

export async function loadYear(year) {
    console.log('loadYear called with', year);
    const data = await fetchYear(year);
    console.log('loadYear: about to set congressData to', Array.isArray(data) ? 'array-' + data.length : data);
    congressData.set(data);

    fetchYear(year - 1);
    fetchYear(year + 1);
}