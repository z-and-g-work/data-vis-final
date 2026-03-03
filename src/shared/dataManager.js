import { writable } from 'svelte/store';
import * as d3 from 'd3';

export const selectedYear = writable(2024);
export const congressData = writable(loadYear(2024));

export async function loadYear(year) {
    const congressNumber = Math.ceil((year - 1788) / 2);
    const data = await d3.json(`/public/data/by_congress/${congressNumber}.json`);
    congressData.set(data);
}