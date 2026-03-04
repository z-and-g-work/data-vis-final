import { writable } from 'svelte/store';
import * as d3 from 'd3';

export const selectedYear = writable(2024);
export const congressData = writable(null); // this can not stay null

const cache = {};

// Only fetch in the browser, not during SSR
if (typeof window !== 'undefined') {
    fetchYear(2024).then(data => congressData.set(data));
}

async function fetchYear(year) {
    const congressNumber = Math.ceil((year - 1788) / 2);
    if (cache[congressNumber]) {
        return cache[congressNumber]
    };
    const data = await d3.json(`/public/data/by_congress/${congressNumber}.json`);
    cache[congressNumber] = data;
    return data;
};

export async function loadYear(year) {
    const data = await fetchYear(year);
    congressData.set(data);

    fetchYear(year - 1);
    fetchYear(year + 1);
};